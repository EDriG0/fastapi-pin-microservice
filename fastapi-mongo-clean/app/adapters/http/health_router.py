from fastapi import APIRouter, Depends
from app.db.mongodb import get_database

router = APIRouter()

@router.get("/health/db", tags=["health"])
async def health_db(db=Depends(get_database)):
    try:
        await db.command("ping")
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
