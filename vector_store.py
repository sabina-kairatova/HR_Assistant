from chromadb import PersistentClient, EmbeddingFunction, Embeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
import pymupdf 
import json
import torch
import os
import openai
from dotenv import load_dotenv

load_dotenv()
torch.classes.__path__ = []  # Neutralizes the path inspection

MODEL_NAME = 'text-embedding-3-small'
DB_PATH = './.chroma_db'
FAQ_FILE_PATH= './FAQ.json'
SOCIAL_PACKAGE_FILE_PATH = './social_package.pdf'


class Product:
    def __init__(self, name: str, id: str, description: str, type: str, price: float, quantity: int):
        self.name = name
        self.id = id
        self.description = description
        self.type = type
        self.price = price
        self.quantity = quantity

class QuestionAnswerPairs:
    def __init__(self, question: str, answer: str):
        self.question = question
        self.answer = answer

class CustomEmbeddingClass(EmbeddingFunction):
    def __init__(self, model=MODEL_NAME):
        self.model = model
        openai.api_key = os.getenv("OPENAI_API_KEY")
    
    def __call__(self, input_texts: List[str]) -> Embeddings:
        response = openai.embeddings.create(
            input=input_texts,
            model=self.model
        )
        return [item.embedding for item in response.data]
    
class FlowerShopVectorStore:
    def __init__(self):
        db = PersistentClient(path=DB_PATH)
        # db.delete_collection('FAQ')
        # db.delete_collection('Social_package')

        custom_embedding_function = CustomEmbeddingClass(MODEL_NAME)

        self.faq_collection = db.get_or_create_collection(name='FAQ', embedding_function=custom_embedding_function)
        self.social_package_collection = db.get_or_create_collection(name='Social_package', embedding_function=custom_embedding_function)

        if self.faq_collection.count() == 0:
            self._load_faq_collection(FAQ_FILE_PATH)

        if self.social_package_collection.count() == 0:
            self._load_social_package_collection(SOCIAL_PACKAGE_FILE_PATH)

    def _load_faq_collection(self, faq_file_path: str):
        with open(faq_file_path, 'r') as f:
            faqs = json.load(f)

        self.faq_collection.add(
            documents=[faq['question'] for faq in faqs] + [faq['answer'] for faq in faqs],
            ids=[str(i) for i in range(0, 2*len(faqs))],
            metadatas = faqs + faqs
        )

    def _load_social_package_collection(self, social_package_file_path: str):
        text = ""
        with pymupdf.open(social_package_file_path) as doc:
            for page in doc:
                text += page.get_text()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        chunks = splitter.split_text(text)

        self.social_package_collection.add(
            documents=chunks,
            ids = [f"chunk_{i}" for i in range(len(chunks))]
        )

    def query_faqs(self, query: str): 
        return self.faq_collection.query(query_texts=[query], n_results=5)
    
    def query_social_package(self, query: str):
        return self.social_package_collection.query(query_texts=[query], n_results=5)