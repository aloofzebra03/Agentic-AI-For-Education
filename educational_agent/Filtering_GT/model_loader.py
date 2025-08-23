from langchain_google_genai import ChatGoogleGenerativeAI
from educational_agent.Filtering_GT.config         import MODEL_NAME, GOOGLE_API_KEY

def get_filter_llm():
    """
    Returns a dedicated LLM instance for filtering/extraction tasks.
    """
    return ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        api_key=GOOGLE_API_KEY,
        temperature=0.0,            # deterministic extraction
        max_tokens=1024,        # enough to return a section
        transport="rest"
    )