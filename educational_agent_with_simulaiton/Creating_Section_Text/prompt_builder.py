# prompt_builder.py

from educational_agent.Creating_Section_Text.schema import NextSectionChoice

_PROMPT = """
You are an AI tutor. Given this NextSectionChoice schema:
{model_schema}

Current section parameters for the current student:
{params}

Ongoing concept:
{concept}

Use these document excerpts as a base to build the next section of the concept:
{docs}

Generate the section content tailored to the student according to the given section parameters keeping in mind the min and max values from the schema.
Note: The section_name given to you in the section parameters is the name of the section that you need to generate content for.Eg. If the section_name is "Explanation", then you need to generate content for the "Explanation" section only and NOTHING else.
Also ensure that you give only the section content in the output and nothing else.
Be concise and clear in your response, focusing on the key points relevant to the ongoing concept.
In case the document excerpts are an empty string or gibberish then completely ignore and generate content for {params} from scratch.
"""

def build_prompt(ongoing_concept: str, section_params: NextSectionChoice, docs: list):
    # return 'Print Nothing'
    return _PROMPT.format(
        model_schema = NextSectionChoice.model_json_schema(),
        params       = section_params.model_dump_json(),
        concept      = ongoing_concept,
        docs         = docs
    )
