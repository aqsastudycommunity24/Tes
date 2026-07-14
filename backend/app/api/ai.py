"""AI Tutor API routes"""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from app.models.ai import ChatRequest, ChatResponse
from app.db.connection import get_db

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db=None
):
    """
    AI Tutor chat endpoint with optional context injection
    
    Request body:
        - message: User message
        - session_id: Chat session ID
        - context_content_id: Optional content ID for context
    """
    if db is None:
        from app.db.connection import get_db as get_db_sync
        db = get_db_sync()
    
    # TODO: Implement LLM integration
    # For now, return a placeholder response
    
    return {
        "response": "AI Tutor response placeholder. Integration coming in Phase 4.",
        "session_id": request.session_id
    }
