from educational_agent.Filtering_GT.model_loader    import get_filter_llm
from educational_agent.Filtering_GT.prompt_builder  import build_filter_prompt

def filter_relevant_section(ongoing_concept: str,
                            section_name,
                            document_full_text: str) -> str:
    prompt = build_filter_prompt(
        ongoing_concept=ongoing_concept,
        section_name=section_name,
        document_full_text=document_full_text
    )
    llm = get_filter_llm()
    response = llm.invoke(prompt)
    # print('Reached here')
    return response.content