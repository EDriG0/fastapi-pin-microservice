from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from .schemas import PinIn, PinOut
from .auth_router import get_current_user

router = APIRouter()

def get_pins_service(request: Request):
    return request.app.container.pin_service

@router.post("/", response_model=PinOut)
async def create_pin(body: PinIn, user=Depends(get_current_user), svc=Depends(get_pins_service)):
    try:
        pin = await svc.create_pin(body.title, body.description, body.image_url, user, body.tags)
        return PinOut(id=pin.id, title=pin.title, description=pin.description, image_url=pin.image_url,
                      author=pin.author, tags=pin.tags, created_at=pin.created_at, updated_at=pin.updated_at)
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("/", response_model=List[PinOut])
async def list_pins(user=Depends(get_current_user), svc=Depends(get_pins_service)):
    pins = await svc.list_pins()
    return [PinOut(id=p.id, title=p.title, description=p.description, image_url=p.image_url,
                   author=p.author, tags=p.tags, created_at=p.created_at, updated_at=p.updated_at) for p in pins]

@router.get("/{pin_id}", response_model=PinOut)
async def get_pin(pin_id: str, user=Depends(get_current_user), svc=Depends(get_pins_service)):
    try:
        p = await svc.get_pin(pin_id)
        return PinOut(id=p.id, title=p.title, description=p.description, image_url=p.image_url,
                      author=p.author, tags=p.tags, created_at=p.created_at, updated_at=p.updated_at)
    except KeyError:
        raise HTTPException(404, "not found")

@router.put("/{pin_id}", response_model=PinOut)
async def update_pin(pin_id: str, body: PinIn, user=Depends(get_current_user), svc=Depends(get_pins_service)):
    try:
        p = await svc.update_pin(pin_id, body.title, body.description, body.image_url, body.tags)
        return PinOut(id=p.id, title=p.title, description=p.description, image_url=p.image_url,
                      author=p.author, tags=p.tags, created_at=p.created_at, updated_at=p.updated_at)
    except KeyError:
        raise HTTPException(404, "not found")
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.delete("/{pin_id}")
async def delete_pin(pin_id: str, user=Depends(get_current_user), svc=Depends(get_pins_service)):
    try:
        await svc.delete_pin(pin_id)
        return {"deleted": True}
    except KeyError:
        raise HTTPException(404, "not found")
