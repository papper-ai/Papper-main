from pydantic import BaseModel
from ..config import settings

VAULT_SERVICE_URL = settings.auth_service_url


class VaultEndpoints(BaseModel):
    create_vault: str = f"{VAULT_SERVICE_URL}/create_vault"
    add_document: str = f"{VAULT_SERVICE_URL}/add_document"
    delete_vault: str = f"{VAULT_SERVICE_URL}/delete_vault"
    delete_document: str = f"{VAULT_SERVICE_URL}/delete_document"
    rename_vault: str = f"{VAULT_SERVICE_URL}/rename_vault"
    get_vault_documents: str = f"{VAULT_SERVICE_URL}/get_vault_documents"
    get_users_vaults: str = f"{VAULT_SERVICE_URL}/get_users_vaults"
    get_vault_by_id: str = f"{VAULT_SERVICE_URL}/get_vault_by_id"
    get_document_by_id: str = f"{VAULT_SERVICE_URL}/get_document_by_id"


vault_endpoints: VaultEndpoints = VaultEndpoints()
