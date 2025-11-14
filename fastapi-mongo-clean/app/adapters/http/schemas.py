from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime

class SignupIn(BaseModel):
    email: str
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ItemIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None

class ItemOut(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class PinIn(BaseModel):
    title: str = Field(..., min_length=1, max_length=300)
    description: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    tags: Optional[List[str]] = []

class PinOut(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    author: Optional[str] = None
    tags: List[str]
    created_at: datetime
    updated_at: datetime

class AccountIn(BaseModel):
    username: str
    email: str
    bio: Optional[str] = None
    profile_image: Optional[HttpUrl] = None

class AccountUpdate(BaseModel):
    username: Optional[str] = None
    bio: Optional[str] = None
    profile_image: Optional[HttpUrl] = None

class AccountOut(BaseModel):
    id: str
    username: str
    email: str
    bio: Optional[str]
    profile_image: Optional[HttpUrl]
    created_at: datetime
    updated_at: datetime