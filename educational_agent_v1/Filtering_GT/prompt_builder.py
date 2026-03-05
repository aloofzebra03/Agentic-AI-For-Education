from langchain.prompts import ChatPromptTemplate

def build_filter_prompt(ongoing_concept: str, section_name: str, document_full_text: str) -> str:
    chat_prompt = ChatPromptTemplate.from_messages([
        # System sets the overall behavior
        ("system", "You are an AI assistant that extracts *exact* excerpts from a document based on a user’s query."),
        # User provides the actual query + instructions
        ("user", 
         "Ongoing Concept: {ongoing_concept}\n"
         "Section Name: {section_name}\n\n"
         "Full Document Text:\n"
         "{document_full_text}\n\n"
         "Instructions:\n"
         "- Return *only* the excerpt(s) that directly address the ongoing concept and section name.\n"
         "- If nothing is relevant, reply with exactly: `No relevant excerpt found.`"
         "Answer should be in paragraph form")
    ])

    return chat_prompt.format(
        ongoing_concept=ongoing_concept,
        section_name=section_name,
        document_full_text=document_full_text
    )
