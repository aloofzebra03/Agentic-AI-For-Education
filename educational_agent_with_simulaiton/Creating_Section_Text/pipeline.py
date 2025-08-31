# pipeline.py

from educational_agent.Creating_Section_Text.model_loader    import get_llm
from educational_agent.Creating_Section_Text.retriever      import retrieve_docs
from educational_agent.Creating_Section_Text.prompt_builder import build_prompt
from educational_agent.Creating_Section_Text.schema         import NextSectionChoice
from educational_agent.Creating_Section_Text.vectorstore import build_vectorstore
from educational_agent.Filtering_GT.filter_utils            import filter_relevant_section
import time

def run_one(ongoing_concept: str, section_params: NextSectionChoice):
    docs   = retrieve_docs(ongoing_concept, section_params)
    combined_text = []
    for d in docs:
        print(f"Retrieved doc page_label: {d.metadata['page_label']}")
        combined_text.append(f"# Page: {d.metadata['page_label']}\n{d.page_content}")
    full_doc = "\n---\n".join(combined_text)
    filtered_text = filter_relevant_section(ongoing_concept, section_params.section_name, full_doc)
    # time.sleep(5)  # Give a moment for the spinner to show
    print(filtered_text)
    prompt = build_prompt(ongoing_concept, section_params, filtered_text)
    llm    = get_llm()
    out    = llm.invoke(prompt)
    #out now contains the next section that will be displayed to the student
    print(out.content)
    return out.content

def ingest_and_build_store():
    vs = build_vectorstore()
    if vs is not None:
        print("Vector store built successfully.")

# def run_one_gt(ongoing_concept: str, section_params: NextSectionChoice):
#     docs   = retrieve_docs(ongoing_concept, section_params)
#     answer = ""
#     for d in docs:
#         print(f"Retrieved doc page_label: {d.metadata['page_label']}")
#         answer = answer + "-----------------------------------" + '\n' + f" # Retrieved doc page_label: {d.metadata['page_label']}" + '\n' +  d.page_content
#     return answer

def run_one_gt(ongoing_concept: str, section_params: NextSectionChoice) -> str:
    # 1. Retrieve relevant documents
    docs = retrieve_docs(ongoing_concept, section_params)
    combined_text = []
    for d in docs:
        print(f"Retrieved doc page_label: {d.metadata['page_label']}")
        combined_text.append(f"# Page: {d.metadata['page_label']}\n{d.page_content}")
    full_doc = "\n---\n".join(combined_text)
    print("Full document text length:", len(full_doc))
    filtered_text = filter_relevant_section(ongoing_concept, section_params.section_name, full_doc)
    print("Filtered text length:", len(filtered_text))
    print(filtered_text)
    return filtered_text
