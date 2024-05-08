from pydantic import BaseModel
from ..config import settings


class RagEndpoints(BaseModel):
    graph_answer: str = f"{settings.graph_rag_service.graph_rag_service_url}/answer"
    vector_answer: str = (
        f"{settings.graph_rag_service.vector_rag_service_url}/qa/answer"
    )


rag_endpoints: RagEndpoints = RagEndpoints()
