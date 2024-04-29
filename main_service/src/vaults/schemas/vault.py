import json
from datetime import datetime
from enum import Enum
from typing import Annotated
from .document import Document
from pydantic import BaseModel, UUID4, ConfigDict, model_validator, Field


class VaultType(str, Enum):
    GRAPH = "graph"
    VECTOR = "vector"


class CreateVault(BaseModel):
    vault_name: str
    vault_type: VaultType

    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class CreateVaultRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: UUID4
    vault_name: str
    vault_type: VaultType


class BaseVaultPayload(BaseModel):
    id: UUID4
    name: str
    type: VaultType


class VaultPayloadPreview(BaseVaultPayload):
    pass


class VaultPayload(BaseVaultPayload):
    created_at: datetime
    user_id: UUID4
    documents: list[Document]


class VaultCredentials(BaseModel):
    vault_id: UUID4 = Field(default="d5c2450f-5d6d-4f45-987c-33b1111b9c8c")


class DocumentCredentials(VaultCredentials):
    document_id: UUID4 = Field(default="d5c2450f-5d6d-4f45-987c-33b1111b9c8c")


class UpdateVault(VaultCredentials):
    new_name: Annotated[str, Field(alias="name", max_length=100)]
