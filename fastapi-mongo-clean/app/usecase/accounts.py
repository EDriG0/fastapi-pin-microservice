from typing import List, Optional
from ..domain.repositories import AccountRepository
from ..domain.entities import Account

class AccountService:
    def __init__(self, repo: AccountRepository):
        self.repo = repo

    async def create_account(self, username: str, email: str, bio: Optional[str], profile_image: Optional[str]) -> Account:
        existing = await self.repo.get_by_email(email)
        if existing:
            raise ValueError("Account with this email already exists.")
        account = Account(username=username, email=email, bio=bio, profile_image=profile_image)
        return await self.repo.create(account)

    async def list_accounts(self) -> List[Account]:
        return await self.repo.list()

    async def get_account(self, account_id: str) -> Account:
        acc = await self.repo.get_by_id(account_id)
        if not acc:
            raise KeyError("Account not found")
        return acc

    async def update_account(self, account_id: str, username: Optional[str], bio: Optional[str], profile_image: Optional[str]) -> Account:
        acc = await self.get_account(account_id)
        acc.update(username, bio, profile_image)
        return await self.repo.update(acc)

    async def delete_account(self, account_id: str) -> bool:
        ok = await self.repo.delete(account_id)
        if not ok:
            raise KeyError("Account not found")
        return ok