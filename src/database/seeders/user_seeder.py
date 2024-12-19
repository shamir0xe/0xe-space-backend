from pylib_0xe.config.config import Config

from src.repositories.repository import Repository
from src.models.user import User
from src.facades.password_facade import PasswordFacade
from .base_seeder import BaseSeeder


class UserSeeder(BaseSeeder):
    def seed(self):
        users = Config.read_env("seeders.users")
        for user in users:
            model = User(**user)
            model.password = PasswordFacade.hash(model.password)
            Repository(User).create(model)
