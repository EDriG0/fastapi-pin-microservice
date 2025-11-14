from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class Item:
    id: Optional[str] = None
    name: str = ""
    description: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def rename(self, new_name: str, new_desc: Optional[str] = None):
        if not new_name or len(new_name) > 200:
            raise ValueError("invalid name")
        self.name = new_name
        self.description = new_desc
        self.updated_at = datetime.utcnow()

@dataclass
class Pin:
    id: Optional[str] = None
    title: str = ""
    description: Optional[str] = None
    image_url: Optional[str] = None
    author: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def update(self, title: str, description: Optional[str], image_url: Optional[str], tags: Optional[List[str]]):
        # simple validation: title required and reasonably sized
        if not title or len(title) > 300:
            raise ValueError("invalid title")
        self.title = title
        self.description = description
        self.image_url = image_url
        self.tags = tags or []
        self.updated_at = datetime.utcnow()

@dataclass
class Account:
    id: Optional[str] = None
    username: str = ""
    email: str = ""
    bio: Optional[str] = None
    profile_image: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def update(self, username: Optional[str], bio: Optional[str], profile_image: Optional[str]):
        if username:
            self.username = username
        if bio is not None:
            self.bio = bio
        if profile_image is not None:
            self.profile_image = profile_image
        self.updated_at = datetime.utcnow()