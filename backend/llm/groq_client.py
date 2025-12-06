from langchain_groq import ChatGroq
from backend.config import settings

def get_groq_client(model: str = None, temperature: float = 0.7):
    """
    Returns a configured ChatGroq client.
    """
    model_name = model or settings.GROQ_MODEL
    
    llm = ChatGroq(
        groq_api_key=settings.GROQ_API_KEY,
        model_name=model_name,
        temperature=temperature
    )
    return llm

def get_llm_scout():
    """
    Returns the 'Scout' LLM instance, optimized for reasoning or specific tasks if configured.
    For now, maps to the main Groq model.
    """
    return get_groq_client(temperature=0.2) # Lower temp for more deterministic tasks
