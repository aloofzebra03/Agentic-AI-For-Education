from pydantic import BaseModel

class ConceptPkg(BaseModel):
    title: str

concept_pkg = ConceptPkg(title="Pendulum and its Time Period")

