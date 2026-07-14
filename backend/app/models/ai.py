"""AI model and schema"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class MessageSchema(BaseModel):
    """Single message schema"""
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatRequest(BaseModel):
    """Chat request schema"""
    message: str
    session_id: str
    context_content_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response schema"""
    response: str
    session_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ConversationSchema(BaseModel):
    """Conversation schema"""
    id: Optional[str] = Field(default=None, alias="_id")
    user_session: str
    messages: List[MessageSchema] = Field(default_factory=list)
    context_content_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
