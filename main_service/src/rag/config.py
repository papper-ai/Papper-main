from pydantic import HttpUrl, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

RAG_SERVICE_DIR = Path(__file__).parent


class GraphRagServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=RAG_SERVICE_DIR / ".env", extra="ignore")
    graph_rag_service_host: str
    graph_rag_service_port: int

    @property
    def graph_rag_service_url(self) -> HttpUrl:
        return f"http://{self.graph_rag_service_host}:{self.graph_rag_service_port}"


class VectorRagServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=RAG_SERVICE_DIR / ".env", extra="ignore")
    vector_rag_service_host: str
    vector_rag_service_port: int

    @property
    def vector_rag_service_url(self) -> HttpUrl:
        return f"http://{self.vector_rag_service_host}:{self.vector_rag_service_port}"


class Setting(BaseModel):
    vector_rag_service: VectorRagServiceSettings = VectorRagServiceSettings()
    graph_rag_service: GraphRagServiceSettings = GraphRagServiceSettings()


settings = Setting()
