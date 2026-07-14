"""Content API routes (public)"""

from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional, List
from app.models.content import ContentResponse, ContentPillar
from app.db.connection import get_db
from bson import ObjectId

router = APIRouter()


@router.get("/", response_model=List[ContentResponse])
async def list_contents(
    pillar: Optional[ContentPillar] = Query(None),
    category: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db=None
):
    """
    List all published contents with filters
    
    Query parameters:
        - pillar: Filter by pillar (quran, hadith, tafsir, sirah)
        - category: Filter by category
        - q: Search query in title
        - page: Page number (default: 1)
        - limit: Items per page (default: 10, max: 100)
    """
    if db is None:
        from app.db.connection import get_db as get_db_sync
        db = get_db_sync()
    
    # Build filter query
    filter_query = {"status": "published", "deleted_at": None}
    
    if pillar:
        filter_query["pillar"] = pillar.value
    
    if category:
        filter_query["category"] = category
    
    if q:
        filter_query["title"] = {"$regex": q, "$options": "i"}
    
    # Calculate skip
    skip = (page - 1) * limit
    
    # Query contents
    contents = await db["contents"].find(filter_query).skip(skip).limit(limit).to_list(limit)
    
    return [
        {
            **content,
            "id": str(content["_id"])
        }
        for content in contents
    ]


@router.get("/{slug}", response_model=ContentResponse)
async def get_content_by_slug(slug: str, db=None):
    """
    Get content by slug
    """
    if db is None:
        from app.db.connection import get_db as get_db_sync
        db = get_db_sync()
    
    content = await db["contents"].find_one({
        "slug": slug,
        "status": "published",
        "deleted_at": None
    })
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    return {
        **content,
        "id": str(content["_id"])
    }
