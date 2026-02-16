from pydantic import BaseModel

class ConceptPkg(BaseModel):
    title: str

# Used by revision agent to specify chapter for revision
