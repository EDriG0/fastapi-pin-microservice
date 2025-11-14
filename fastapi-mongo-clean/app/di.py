from typing import Optional
from app.infrastructure.db import Database
from app.infrastructure.security import AuthService
from app.adapters.repo.mongo_item_repo import MongoItemRepository
from app.usecase.items import ItemService
from app.adapters.repo.mongo_pin_repo import MongoPinRepository
from app.usecase.pins import PinService
from app.adapters.repo.mongo_account_repo import MongoAccountRepository
from app.usecase.accounts import AccountService

class Container:
    def __init__(self):
        self._db: Optional[Database] = None
        self._auth: Optional[AuthService] = None
        self._item_service: Optional[ItemService] = None
        self._account_service: Optional[AccountService] = None
        self._pin_service: Optional[PinService] = None

    @property
    def db(self) -> Database:
        if self._db is None:
            self._db = Database()
        return self._db

    @property
    def auth(self) -> AuthService:
        if self._auth is None:
            self._auth = AuthService()
        return self._auth

    @property
    def item_service(self) -> ItemService:
        if self._item_service is None:
            self._item_service = ItemService(MongoItemRepository(self.db))
        return self._item_service

    @property
    def pin_service(self) -> PinService:
        if self._pin_service is None:
            self._pin_service = PinService(MongoPinRepository(self.db))
        return self._pin_service

    @property
    def account_service(self) -> AccountService:
        if self._account_service is None:
            self._account_service = AccountService(MongoAccountRepository(self.db))
        return self._account_service

