from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

class TagBase(BaseModel):
    name: str = Field(..., max_length=50)

class TagCreate(TagBase):
    pass

class TagOut(TagBase):
    id: int
    class Config:
        from_attributes = True

class NoteBase(BaseModel):
    title: str = Field(..., max_length=200)
    content: str = ""

class NoteCreate(NoteBase):
    tags: Optional[List[str]] = None  # tag names

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_archived: Optional[bool] = None
    tags: Optional[List[str]] = None

class NoteOut(NoteBase):
    id: int
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    tags: List[TagOut] = []
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
