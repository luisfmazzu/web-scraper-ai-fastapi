from app.config import database
from .repository.repository import AuthRepository


class Service:
    def __init__(self):
        self.database = database
        self.auth_repository = AuthRepository(self.database)


def get_service():
    return svc


svc = Service()
