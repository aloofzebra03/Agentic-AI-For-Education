import os
from educational_agent.Creating_Section_Text import config
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)

def get_embedder():
    print("Building Gemini embedder...")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",  
        # google_api_key=st.secrets['GOOGLE_API_KEY'] 
    )
    # sanity check
    vec = embeddings.embed_query("hello, world!")
    print("Test Vector length:", len(vec))
    return embeddings

