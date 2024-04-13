from pydantic import BaseModel, UUID4


class Bibki(BaseModel):
    bibki: str
    id: UUID4
    name: str
