import os

# Make sure we never import TensorFlow or Flax via `transformers`
os.environ["TRANSFORMERS_NO_TF"] = "1"
os.environ["TRANSFORMERS_NO_FLAX"] = "1"

from educational_agent_v1.Creating_Section_Text import config
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)

def get_embedder():
    print("Building HuggingFace embeddinggemma-300m embedder...")
    print()
    embeddings = HuggingFaceEmbeddings(
        model_name="google/embeddinggemma-300m",
        query_encode_kwargs={"prompt_name": "query"},
        encode_kwargs={"prompt_name": "document"}
    )
    # sanity check
    vec = embeddings.embed_query("hello, world!")
    print("Test Vector length:", len(vec))
    return embeddings

