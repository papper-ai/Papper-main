from pydantic import BaseModel
from ..config import settings


class GraphRagEndpoints(BaseModel):
    get_answer: str = f"{settings.graph_rag_service.graph_rag_service_url}/answer"


graph_rag_endpoints: GraphRagEndpoints = GraphRagEndpoints()
