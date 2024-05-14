from pydantic import BaseModel
from ..config import settings

HISTORY_SERVICE_URL = settings.history_service_settings.history_service_url
CHATS_SERVICE_URL = settings.chats_service_settings.chats_service_url


class ChatsEndpoints(BaseModel):
    create_chat: str = f"{CHATS_SERVICE_URL}/create_chat"
    delete_chat: str = f"{CHATS_SERVICE_URL}/delete_chat"
    set_chat_name: str = f"{CHATS_SERVICE_URL}/set_chat_name"
    get_user_chats: str = f"{CHATS_SERVICE_URL}/get_user_chats"
    get_user_archived_chats: str = f"{CHATS_SERVICE_URL}/get_user_archived_chats"
    get_chat_by_id: str = f"{CHATS_SERVICE_URL}/get_chat_by_id"
    archive_chat: str = f"{CHATS_SERVICE_URL}/archive_chat"
    unarchive_chat: str = f"{CHATS_SERVICE_URL}/unarchive_chat"
    get_vault_chats: str = f"{CHATS_SERVICE_URL}/get_vault_chats"


class HistoryEndpoints(BaseModel):
    create_message: str = f"{HISTORY_SERVICE_URL}/create_history"
    add_user_message: str = f"{HISTORY_SERVICE_URL}/add_user_message"
    add_ai_message: str = f"{HISTORY_SERVICE_URL}/add_ai_message"
    clear_history: str = f"{HISTORY_SERVICE_URL}/clear_history"
    delete_history: str = f"{HISTORY_SERVICE_URL}/delete_history"
    get_history: str = f"{HISTORY_SERVICE_URL}/get_history"


chats_endpoints: ChatsEndpoints = ChatsEndpoints()
history_endpoints: HistoryEndpoints = HistoryEndpoints()
