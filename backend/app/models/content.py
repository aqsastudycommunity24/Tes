"""Content model and schema"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ContentPillar(str, Enum):
    """Content pillar enumeration"""
    QURAN = "quran"
    HADITH = "hadith"
    TAFSIR = "tafsir"
    SIRAH = "sirah"


class ContentStatus(str, Enum):
    """Content status enumeration"""
    DRAFT = "draft"
    PUBLISHED = "published"


class ContentBase(BaseModel):
    """Base content schema"""
    pillar: ContentPillar
    title: str = Field(..., min_length=1, max_length=500)
    category: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    tags: List[str] = Field(default_factory=list)
    status: ContentStatus = ContentStatus.DRAFT


class ContentCreate(ContentBase):
    """Content creation schema"""
    html_body: str
    cover_image: Optional[str] = None


class ContentUpdate(BaseModel):
    """Content update schema"""
    title: Optional[str] = None
    category: Optional[str] = None
    slug: Optional[str] = None
    html_body: Optional[str] = None
    tags: Optional[List[str]] = None
    cover_image: Optional[str] = None
    status: Optional[ContentStatus] = None


class ContentResponse(ContentBase):
    """Content response schema"""
    id: str = Field(alias="_id")
    html_body: str
    cover_image: Optional[str] = None
    author_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True


class Content(ContentBase):
    """Content database model"""
    id: Optional[str] = Field(default=None, alias="_id")
    html_body: str
    cover_image: Optional[str] = None
    author_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = None
    
    class Config:
        populate_by_name = True
