from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from .schemas import AccountIn, AccountOut, AccountUpdate
from .auth_router import get_current_user

router = APIRouter()

def get_account_service(request: Request):
    return request.app.container.account_service

@router.post("/", response_model=AccountOut)
async def create_account(body: AccountIn, user=Depends(get_current_user), svc=Depends(get_account_service)):
    try:
        acc = await svc.create_account(body.username, body.email, body.bio, body.profile_image)
        return acc
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("/", response_model=List[AccountOut])
async def list_accounts(user=Depends(get_current_user), svc=Depends(get_account_service)):
    return await svc.list_accounts()

@router.get("/{account_id}", response_model=AccountOut)
async def get_account(account_id: str, user=Depends(get_current_user), svc=Depends(get_account_service)):
    try:
        return await svc.get_account(account_id)
    except KeyError:
        raise HTTPException(404, "Not found")

@router.put("/{account_id}", response_model=AccountOut)
async def update_account(account_id: str, body: AccountUpdate, user=Depends(get_current_user), svc=Depends(get_account_service)):
    try:
        return await svc.update_account(account_id, body.username, body.bio, body.profile_image)
    except KeyError:
        raise HTTPException(404, "Not found")

@router.delete("/{account_id}")
async def delete_account(account_id: str, user=Depends(get_current_user), svc=Depends(get_account_service)):
    try:
        await svc.delete_account(account_id)
        return {"deleted": True}
    except KeyError:
        raise HTTPException(404, "Not found")