from pydantic import BaseModel, HttpUrl
from datetime import datetime

class UrlCreate(BaseModel):
    original_url: HttpUrl

class UrlResponse(BaseModel):
    short_code: str
    original_url: str

    class Config:
        from_attributes = True

class UrlStats(BaseModel):
    short_code: str
    original_url: str
    clicks: int
    created_at: datetime

    class Config:
        from_attributes = True
