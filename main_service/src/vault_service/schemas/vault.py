import json
from datetime import datetime
from enum import Enum
from typing import Annotated
from uuid import uuid4

from fastapi import UploadFile
from pydantic import BaseModel, UUID4, ConfigDict, model_validator, Field


class VaultType(str, Enum):
    GRAPH = "graph"
    VECTOR = "vector"


class BaseVault(BaseModel):
    vault_name: str
    vault_type: VaultType

    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class VaultCredentials(BaseVault):
    pass


class CreateVault(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: UUID4
    vault_name: str
    vault_type: VaultType


class VaultResponse(BaseVault):
    id: UUID4
    name: str
    type: VaultType
    created_at: datetime
    user_id: UUID4


class UpdateVault(BaseModel):
    vault_id: UUID4 = Field(default="68f7a831769442baae77c7de4974b67f")
    new_name: str
