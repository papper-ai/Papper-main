from pydantic import BaseModel, UUID4


class Document(BaseModel):
    id: UUID4
    name: str
    text: str
    vault_id: UUID4
