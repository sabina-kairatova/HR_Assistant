from langchain_core.tools import tool
from typing import List, Dict
from vector_store import FlowerShopVectorStore


vector_store = FlowerShopVectorStore()

@tool
def query_knowledge_base(query: str) -> List[Dict[str, str]]:
    """
    Ищет информацию на базе знаний, которая поможет ответить на часто задавамые вопросы сотрудников и получить информацию об оформления документов.

    Args:
        query (str): Вопрос к базе знаний

    Return:
        List[Dict[str, str]]: Потенциально релевантные пары вопросов и ответов из базы знаний
    """
    return vector_store.query_faqs(query=query)



@tool
def search_for_social_package_information(query: str):
    """
    Ищет информацию в базе знаний, чтобы помочь сотрудникам с вопросами касаемо социального пакета.

    Args:
        query (str): Вопрос к базе знаний

    Return:
        List[Dict[str, str]]: Потенциально релевантные ответы из базы знаний
    """
    return vector_store.query_inventories(query=query)



