from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: UUID
    username: str


class TokenData(BaseModel):
    username: Optional[str] = None
