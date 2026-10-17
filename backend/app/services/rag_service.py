import json
import os
import faiss
import numpy as np
import openai
from sentence_transformers import SentenceTransformer
from app.config import get_settings

class RAGService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=get_settings().OPENAI_API_KEY)
        self.model = get_settings().LLM_MODEL
        # Initialize sentence transformer and FAISS index
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.chunks = []
        self._load_and_index()
        
    def _load_and_index(self):
        chunks_path = os.path.join(os.path.dirname(__file__), "..", "data", "schemes", "pm_kisan_rag_chunks.json")
        try:
            with open(chunks_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.chunks = data.get("chunks", [])
                
                if self.chunks:
                    # Create embeddings
                    texts = [chunk["content"] for chunk in self.chunks]
                    embeddings = self.encoder.encode(texts)
                    
                    # Create FAISS index
                    dimension = embeddings.shape[1]
                    self.index = faiss.IndexFlatL2(dimension)
                    self.index.add(np.array(embeddings).astype('float32'))
        except FileNotFoundError:
            print("Warning: pm_kisan_rag_chunks.json not found. RAG will not have scheme data context.")
            
    def _search(self, query: str, k: int = 3) -> list:
        if not self.index or not self.chunks:
            return []
            
        query_embedding = self.encoder.encode([query])
        distances, indices = self.index.search(np.array(query_embedding).astype('float32'), k)
        
        results = []
        for idx in indices[0]:
            if idx < len(self.chunks):
                results.append(self.chunks[idx]["content"])
        return results

    async def evaluate_eligibility(self, fields: dict) -> dict:
        """Evaluate PM-KISAN eligibility using RAG and LLM."""
        
        # Format the fields into a query text
        farmer_context = json.dumps(fields, ensure_ascii=False)
        query = f"Farmer details: {farmer_context}. What are the PM-KISAN eligibility and exclusion criteria?"
        
        # Retrieve relevant chunks
        relevant_chunks = self._search(query, k=5)
        context = "\n\n".join(relevant_chunks)
        
        system_prompt = """You are an expert government scheme eligibility evaluator for PM-KISAN.
You must strictly follow the scheme guidelines and evaluate if the farmer is eligible.

Exclusion Categories (Strictly Disqualified if ANY apply):
1. Institutional landholders
2. Former or present constitutional post holders
3. Former or present Ministers/State Ministers, Mayors, Zila Parishad Chairpersons, MLAs, MLCs, MPs
4. All serving or retired officers and employees of Central/State Government Ministries/Offices/Departments (except Multi Tasking Staff / Class IV / Group D)
5. All superannuated/retired pensioners whose monthly pension is ₹10,000/- or more (except Multi Tasking Staff / Class IV / Group D)
6. All Persons who paid Income Tax in last assessment year
7. Professionals like Doctors, Engineers, Lawyers, Chartered Accountants, and Architects registered with Professional bodies and carrying out profession by undertaking practices.

Eligibility Requirements:
1. Must be a farmer with cultivable landholding in their name.
2. If total land is zero, they are disqualified.

Input: 
1. Scheme Context (Retrieved Rules)
2. Farmer Details (JSON)

Output JSON Format:
{
    "eligible": true/false,
    "reasons": ["List of specific reasons for eligibility or disqualification"],
    "missing_fields": ["List of fields required to make a full determination, if any"],
    "explanation": "A simple explanation in Hindi that can be read out to the farmer"
}
"""

        user_prompt = f"Scheme Context:\n{context}\n\nFarmer Details:\n{farmer_context}"
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return {
            "eligible": result.get("eligible", False),
            "reasons": result.get("reasons", []),
            "missing_fields": result.get("missing_fields", []),
            "explanation": result.get("explanation", "")
        }
