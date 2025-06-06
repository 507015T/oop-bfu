from typing import Protocol
from protocols.data import DataRepositoryProtocol
from schemas.users import User


class UserRepositoryProtocol(DataRepositoryProtocol[User], Protocol):
    def get_by_login(self, login: str) -> User | None: ...
