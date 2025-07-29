
from Creating_Section_Text.vectorstore import load_vectorstore
from Creating_Section_Text.schema import NextSectionChoice

def build_query_text(ongoing_concept: str, section_name: str) -> str:
    return (
        f"Find me all pages in the PDF about the concept “{ongoing_concept}” "
        f"that cover the section titled “{section_name}.”"
    )

def retrieve_docs(ongoing_concept: str,
                  section_params: NextSectionChoice,
                  k: int = 2):
    vs    = load_vectorstore()
    query = build_query_text(ongoing_concept, section_params.section_name)
    docs =  vs.similarity_search(query, k=k)
    print(f"Retrieved {len(docs)} documents for query: {query}")
    return docs
