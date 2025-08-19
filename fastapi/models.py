from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class URLCreate(BaseModel):
    original_url: str
    custom_code: Optional[str] = None


class URLResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    short_url: str
    created_at: datetime
    click_count: int


class URLStats(BaseModel):
    id: int
    original_url: str
    short_code: str
    short_url: str
    created_at: datetime
    click_count: int
    last_accessed: Optional[datetime] = None
