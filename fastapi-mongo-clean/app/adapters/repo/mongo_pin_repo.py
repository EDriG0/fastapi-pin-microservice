from typing import List, Optional
from bson import ObjectId
from ...domain.entities import Pin
from ...domain.repositories import PinRepository
from ...infrastructure.db import Database

class MongoPinRepository(PinRepository):
    def __init__(self, db: Database):
        self.db = db

    async def _coll(self):
        d = await self.db.db()
        return d.get_collection("pins")

    def _map(self, d) -> Pin:
        return Pin(
            id=str(d.get("_id")),
            title=d.get("title"),
            description=d.get("description"),
            image_url=d.get("image_url"),
            author=d.get("author"),
            tags=d.get("tags") or [],
            created_at=d.get("created_at"),
            updated_at=d.get("updated_at"),
        )

    async def create(self, pin: Pin) -> Pin:
        coll = await self._coll()
        doc = {
            "title": pin.title,
            "description": pin.description,
            "image_url": pin.image_url,
            "author": pin.author,
            "tags": pin.tags,
            "created_at": pin.created_at,
            "updated_at": pin.updated_at,
        }
        res = await coll.insert_one(doc)
        pin.id = str(res.inserted_id)
        return pin

    async def list(self) -> List[Pin]:
        coll = await self._coll()
        cur = coll.find({})
        items = []
        async for d in cur:
            items.append(self._map(d))
        return items

    async def get(self, pin_id: str) -> Optional[Pin]:
        coll = await self._coll()
        try:
            oid = ObjectId(pin_id)
        except Exception:
            return None
        d = await coll.find_one({"_id": oid})
        if not d:
            return None
        return self._map(d)

    async def update(self, pin: Pin) -> Pin:
        coll = await self._coll()
        try:
            oid = ObjectId(pin.id)
        except Exception:
            raise ValueError("invalid id")
        await coll.update_one({"_id": oid}, {"$set": {
            "title": pin.title,
            "description": pin.description,
            "image_url": pin.image_url,
            "tags": pin.tags,
            "updated_at": pin.updated_at,
        }})
        return pin

    async def delete(self, pin_id: str) -> bool:
        coll = await self._coll()
        try:
            oid = ObjectId(pin_id)
        except Exception:
            return False
        res = await coll.delete_one({"_id": oid})
        return bool(res.deleted_count)