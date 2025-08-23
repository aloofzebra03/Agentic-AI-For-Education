from pydantic import BaseModel
from typing import List

class ConceptPkg(BaseModel):
    title: str

concept_pkg = ConceptPkg(title="Simple Pendulum")

