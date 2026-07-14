"""Admin panel API routes"""

from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from typing import Optional, List
from app.models.content import ContentCreate, ContentUpdate, ContentResponse
from app.models.user import UserResponse, UserCreate, UserUpdate
from app.db.connection import get_db
import bleach
from bson import ObjectId

router = APIRouter()

# Allowed HTML tags and attributes for sanitization
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li', 'div', 'span', 'a', 'blockquote', 'img', 'table',
    'thead', 'tbody', 'tr', 'td', 'th'
]
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'img': ['src', 'alt', 'title', 'width', 'height'],
    'div': ['class'],
    'span': ['class'],
    'table': ['class'],
}


def sanitize_html(html_content: str) -> str:
    """Sanitize HTML content"""
    return bleach.clean(
        html_content,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True
    )


@router.post("/contents", response_model=ContentResponse)
async def create_content(
    content_data: ContentCreate,
    db=None
):
    """
    Create new content (admin only)
    """
    if db is None:
        from app.db.connection import get_db as get_db_sync
        db = get_db_sync()
    
    # Sanitize HTML
    sanitized_html = sanitize_html(content_data.html_body)
    
    # Check if slug already exists
    existing = await db["contents"].find_one({"slug": content_data.slug})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Content with this slug already exists"
        )
    
    # Create content document
    content_doc = {
        **content_data.dict(),
        "html_body": sanitized_html,
        "pillar": content_data.pillar.value,
        "status": content_data.status.value,
        "author_id": "system",  # Should be current user
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "deleted_at": None
    }
    
    result = await db["contents"].insert_one(content_doc)
    
    return {
        **content_doc,
        "id": str(result.inserted_id)
    }


@router.put("/contents/{content_id}", response_model=ContentResponse)
async def update_content(
    content_id: str,
    content_data: ContentUpdate,
    db=None
):
    """
    Update content (admin only)
    """
    if db is None:
        from app.db.connection import get_db as get_db_sync
        db = get_db_sync()
    
    try:
        obj_id = ObjectId(content_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid content ID"
        )
    
    # Prepare update data
    update_data = {k: v for k, v in content_data.dict().items() if v is not None}
    
    if "html_body" in update_data:
        update_data["html_body"] = sanitize_html(update_data["html_body"])
    
    if "pillar" in update_data:
        update_data["pillar"] = update_data["pillar"].value
    
    if "status" in update_data:
        update_data["status"] = update_data["status"].value
    
    update_data["updated_at"] = datetime.utcnow()
    
    # Update content
    result = await db["contents"].find_one_and_update(
        {"_id": obj_id},
        {"$set": update_data},
        return_document=True
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    return {
        **result,
        "id": str(result["_id"])
    }


@router.delete("/contents/{content_id}")
async def delete_content(content_id: str, db=None):
    """
    Soft delete content
    """
    if db is None:
        from app.db.connection import get_db as get_db_sync
        db = get_db_sync()
    
    try:
        obj_id = ObjectId(content_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid content ID"
        )
    
    result = await db["contents"].find_one_and_update(
        {"_id": obj_id},
        {"$set": {"deleted_at": datetime.utcnow()}},
        return_document=True
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    return {"message": "Content deleted successfully"}


@router.post("/upload-html")
async def upload_html_file(file: UploadFile = File(...)):
    """
    Upload and parse HTML file
    """
    try:
        content = await file.read()
        html_string = content.decode("utf-8")
        
        # Extract body content or use whole file
        if "<body>" in html_string:
            start = html_string.find("<body>") + 6
            end = html_string.find("</body>")
            html_content = html_string[start:end]
        else:
            html_content = html_string
        
        # Sanitize
        sanitized = sanitize_html(html_content)
        
        return {
            "filename": file.filename,
            "html_content": sanitized,
            "size": len(sanitized)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error processing file: {str(e)}"
        )


from datetime import datetime
