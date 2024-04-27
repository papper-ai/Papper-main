import json
from datetime import datetime
from enum import Enum
from typing import Annotated
from uuid import uuid4
from .document import Document
from fastapi import UploadFile
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


class BaseVaultRequest(BaseModel):
    vault_id: UUID4 = Field(default="d5c2450f-5d6d-4f45-987c-33b1111b9c8c")


class BaseVaultCredentials(BaseModel):
    id: UUID4
    name: str
    type: VaultType


class PreviewVaultCredentials(BaseVaultCredentials):
    pass


class VaultCredentials(BaseVaultCredentials):
    created_at: datetime
    user_id: UUID4
    documents: list[Document]


class CreateVaultResponse(VaultCredentials):
    pass


class AddDocumentRequest(BaseVaultRequest):
    pass


class UpdateVault(BaseVaultRequest):
    new_name: str


class UpdateVaultRequest(BaseVaultRequest):
    name: str


class DeleteVaultRequest(BaseVaultRequest):
    pass


class DeleteDocumentRequest(BaseVaultRequest):
    document_id: UUID4 = Field(default="d7a2476a1b9a4232b0475cbd4c250bf6")


class GetVaultDocumentsRequest(BaseVaultRequest):
    pass


class GetVaultRequest(BaseVaultRequest):
    pass


class GetDocumentRequest(BaseModel):
    document_id: UUID4


class GetUserVaultsRequest(BaseModel):
    user_id: UUID4
