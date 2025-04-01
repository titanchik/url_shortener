from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class LinkBase(BaseModel):
    original_url: HttpUrl
    custom_alias: Optional[str] = None
    expires_at: Optional[datetime] = None

class LinkCreate(LinkBase):
    pass

class Link(LinkBase):
    short_code: str
    created_at: datetime
    clicks: int
    last_clicked_at: Optional[datetime]
    
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    
    class Config:
        orm_mode = True