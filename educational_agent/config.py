# agent/config.py
from pydantic import BaseModel
from typing import List

# class ConceptPkg(BaseModel):
#     title: str
#     hook_question: str
#     one_line_definition: str
#     mechanism_question: str
#     common_misconceptions: List[str]
#     misconception_correction: str
#     real_life_fact: str
#     transfer_question: str

# concept_pkg = ConceptPkg(
#     title="Oscillatory Motion",
#     hook_question="Think of a child's swing. What would you call that kind of motion?",
#     one_line_definition="An oscillatory motion repeats in equal time intervals.",
#     mechanism_question="Why doesn’t the swing just stop in the middle? What pulls it back?",
#     common_misconceptions=["A heavier child swings faster."],
#     misconception_correction="Mass does not affect the oscillation period; chain length does.",
#     real_life_fact="Pendulums were used in clocks to mark seconds precisely.",
#     transfer_question="If there were no gravity, would a pendulum still swing?"
# )

class ConceptPkg(BaseModel):
    title: str

# Now we only need the concept title;
# all prompts (hook, definition, mechanism, etc.) are generated dynamically.
concept_pkg = ConceptPkg(title="educational_agent/nodes4_rag.py")

