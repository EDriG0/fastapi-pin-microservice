from typing import List, Optional
from ..domain.repositories import PinRepository

try:
    from ..domain.entities import Pin as PinEntity
except Exception:
    from ..domain.entities import Pin as PinEntity

class PinService:
    def __init__(self, repo: PinRepository):
        self.repo = repo

    async def create_pin(self, title: str, description: Optional[str], image_url: Optional[str], author: Optional[str], tags: Optional[List[str]]) -> PinEntity:
        pin = PinEntity(title=title, description=description, image_url=image_url, author=author, tags=tags or [])
        if not pin.title:
            raise ValueError("title required")
        return await self.repo.create(pin)

    async def list_pins(self) -> List[PinEntity]:
        return await self.repo.list()

    async def get_pin(self, pin_id: str) -> PinEntity:
        pin = await self.repo.get(pin_id)
        if not pin:
            raise KeyError("not found")
        return pin

    async def update_pin(self, pin_id: str, title: str, description: Optional[str], image_url: Optional[str], tags: Optional[List[str]]) -> PinEntity:
        pin = await self.get_pin(pin_id)
        pin.update(title, description, image_url, tags)
        return await self.repo.update(pin)

    async def delete_pin(self, pin_id: str) -> bool:
        ok = await self.repo.delete(pin_id)
        if not ok:
            raise KeyError("not found")
        return ok
