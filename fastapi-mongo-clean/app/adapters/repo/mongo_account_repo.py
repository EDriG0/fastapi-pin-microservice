from typing import List, Optional
from bson import ObjectId
from ...domain.entities import Account
from ...domain.repositories import AccountRepository
from ...infrastructure.db import Database

class MongoAccountRepository(AccountRepository):
    def __init__(self, db: Database):
        self.db = db

    async def _coll(self):
        d = await self.db.db()
        return d.get_collection("accounts")

    def _map(self, d) -> Account:
        return Account(
            id=str(d["_id"]),
            username=d.get("username"),
            email=d.get("email"),
            bio=d.get("bio"),
            profile_image=d.get("profile_image"),
            created_at=d.get("created_at"),
            updated_at=d.get("updated_at"),
        )

    async def create(self, account: Account) -> Account:
        coll = await self._coll()
        doc = account.__dict__.copy()
        doc.pop("id", None)
        res = await coll.insert_one(doc)
        account.id = str(res.inserted_id)
        return account

    async def list(self) -> List[Account]:
        coll = await self._coll()
        cursor = coll.find({})
        accounts = []
        async for d in cursor:
            accounts.append(self._map(d))
        return accounts

    async def get_by_id(self, account_id: str) -> Optional[Account]:
        coll = await self._coll()
        try:
            oid = ObjectId(account_id)
        except:
            return None
        d = await coll.find_one({"_id": oid})
        return self._map(d) if d else None

    async def get_by_email(self, email: str) -> Optional[Account]:
        coll = await self._coll()
        d = await coll.find_one({"email": email})
        return self._map(d) if d else None

    async def update(self, account: Account) -> Account:
        coll = await self._coll()
        oid = ObjectId(account.id)
        await coll.update_one({"_id": oid}, {"$set": {
            "username": account.username,
            "bio": account.bio,
            "profile_image": account.profile_image,
            "updated_at": account.updated_at
        }})
        return account

    async def delete(self, account_id: str) -> bool:
        coll = await self._coll()
        try:
            oid = ObjectId(account_id)
        except:
            return False
        res = await coll.delete_one({"_id": oid})
        return bool(res.deleted_count)
