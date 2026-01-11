from pydantic import BaseModel
from typing import Optional, List

class AskRequest(BaseModel):
    query: str
    session_id: Optional[str] = None

class AskResponse(BaseModel):
    answer: str
    sources: List[str]
