import pandas as pd 
from sentence_transformers import SentenceTransformer, util
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import numpy as np
load_dotenv()

class chat:
    def __init__(self):
        # Load LLM
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-8b-instant"
        )
        
        # Read data
        print("Reading data...")
        self.df_insights = pd.read_csv("data/insights_meta.csv")
        self.ids = self.df_insights["pubmed_id"].astype(str).tolist()
        self.documents = self.df_insights["full_text"].tolist()
        print(f"Loaded {len(self.documents)} documents")
        
        # Load embedding model
        print("Loading embedding model...")

        self.sent_model = SentenceTransformer('all-mpnet-base-v2')
        
        # Create embeddings for all documents (replacing ChromaDB)
        print("Creating embeddings for all documents...")
        self.document_embeddings = self.embedding_model.encode(self.documents)
        print(f"Created embeddings for {len(self.documents)} documents")
    
    def cosine_sim(self, x1, x2):
        """
        Calculate cosine similarity between two texts using sentence-transformers
        
        Args:
            x1 (str): First text
            x2 (str): Second text
            
        Returns:
            float: Cosine similarity score (rounded to 2 decimal places)
        """
        embedding1 = self.sent_model.encode(str(x1), convert_to_tensor=True)
        embedding2 = self.sent_model.encode(str(x2), convert_to_tensor=True)
        similarity = util.cos_sim(embedding1, embedding2)
        return round(similarity.item(), 2)
            
    def answer_(self, question: str, top_k: int = 2) -> str:
        # Encode question
        question_embedding = self.embedding_model.encode([question])[0]
        
        # Calculate similarity scores manually
        similarities = []
        for i, doc in enumerate(self.documents):
            # Use the cosine_sim function instead of direct cosine calculation
            similarity = self.cosine_sim(question, doc)
            similarities.append((i, similarity))
        
        # Sort by similarity (highest first)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Get top k most similar documents
        top_indices = [idx for idx, _ in similarities[:top_k]]
        relevant_docs = [self.documents[idx] for idx in top_indices]
        
        # Create context and prompt
        context = "\n\n".join(relevant_docs)
        
        prompt = f"""You are a biomedical research assistant. 
        Use the following context to answer the question:\n\n{context}\n\n
        Question: {question}\n
        Answer:
        """.strip()
        
        response = self.llm.invoke(prompt)
        return response.content