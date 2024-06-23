import uuid
import json
from ..schemas.document import Document
from ..schemas.vault import VaultPayloadPreview, VaultPayload
from src.repositories.redis import RedisRepository


class VaultsCache:
    def __init__(self, redis_repository: type(RedisRepository)):
        self.redis: RedisRepository = redis_repository()
        self.cache_prefix = "vaults:"
        self.documents_prefix = "documents:"
        self.document_prefix = "document:"
        self.vaults_prefix = "vaults:"
        self.vault_prefix = "vault:"

    async def get_documents(self, vault_id: uuid.UUID) -> None | list[Document]:
        result = await self.redis.get(
            f"{self.cache_prefix}{self.documents_prefix}{vault_id.hex}"
        )
        documents_json = json.loads(result) if result else None
        documents = (
            [Document.model_validate_json(document) for document in documents_json]
            if documents_json
            else None
        )
        return documents

    async def set_documents(
        self, vault_id: uuid.UUID, documents: list[Document]
    ) -> bool:
        documents_json = [document.model_dump_json() for document in documents]
        documents_str = json.dumps(documents_json)
        return await self.redis.set(
            f"{self.cache_prefix}{self.documents_prefix}{vault_id.hex}", documents_str
        )

    async def delete_documents(self, vault_id: uuid.UUID) -> bool:
        return await self.redis.delete(
            f"{self.cache_prefix}{self.documents_prefix}{vault_id.hex}"
        )

    async def get_document(self, document_id: uuid.UUID) -> None | Document:
        result = await self.redis.get(
            f"{self.cache_prefix}{self.document_prefix}{document_id.hex}"
        )
        document = Document.model_validate_json(result) if result else None
        return document

    async def set_document(self, document_id: uuid.UUID, document: Document) -> bool:
        document_str = document.model_dump_json()
        return await self.redis.set(
            f"{self.cache_prefix}{self.document_prefix}{document_id.hex}",
            document_str,
        )

    async def delete_document(self, document_id: uuid.UUID) -> bool:
        return await self.redis.delete(
            f"{self.cache_prefix}{self.document_prefix}{document_id.hex}"
        )

    async def get_vaults_preview(
        self, user_id: uuid.UUID
    ) -> None | list[VaultPayloadPreview]:
        result = await self.redis.get(
            f"{self.cache_prefix}{self.vaults_prefix}{user_id.hex}"
        )
        vaults_preview_json = json.loads(result) if result else None
        vaults_preview = (
            [
                VaultPayloadPreview.model_validate_json(vault)
                for vault in vaults_preview_json
            ]
            if vaults_preview_json
            else None
        )
        return vaults_preview

    async def set_vaults_preview(
        self, user_id: uuid.UUID, vaults_preview: list[VaultPayloadPreview]
    ) -> bool:
        vaults_preview_json = [vault.model_dump_json() for vault in vaults_preview]
        vaults_preview_str = json.dumps(vaults_preview_json)
        return await self.redis.set(
            f"{self.cache_prefix}{self.vaults_prefix}{user_id.hex}", vaults_preview_str
        )

    async def delete_vaults_preview(self, user_id: uuid.UUID) -> bool:
        return await self.redis.delete(
            f"{self.cache_prefix}{self.vaults_prefix}{user_id.hex}"
        )

    async def get_vault(self, vault_id: uuid.UUID) -> None | VaultPayload:
        result = await self.redis.get(
            f"{self.cache_prefix}{self.vault_prefix}{vault_id.hex}"
        )
        vault = VaultPayload.model_validate_json(result) if result else None
        return vault

    async def set_vault(self, vault_id: uuid.UUID, vault_payload: VaultPayload) -> bool:
        vault_str = vault_payload.model_dump_json()
        return await self.redis.set(
            f"{self.cache_prefix}{self.vault_prefix}{vault_id.hex}", vault_str
        )

    async def delete_vault(self, vault_id: uuid.UUID) -> bool:
        return await self.redis.delete(
            f"{self.cache_prefix}{self.vault_prefix}{vault_id.hex}"
        )


vaults_cache_manager = VaultsCache(RedisRepository)
