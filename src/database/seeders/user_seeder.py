import logging
from pylib_0xe.config.config import Config
from src.repositories.user_repository import UserRepository
from src.repositories.repository import Repository
from src.models.user import User
from src.facades.password_facade import PasswordFacade
from .base_seeder import BaseSeeder

LOGGER = logging.getLogger(__name__)


class UserSeeder(BaseSeeder):
    def seed(self):
        users = Config.read_env("seeders.users")
        for user_data in users:
            try:
                # Check if the user exists, so do nothing
                username = user_data["username"]
                UserRepository(User).read_by_username(username)
                LOGGER.info(f"{username} exists!")
            except Exception as e:
                user = User(**user_data)
                user.password = PasswordFacade.hash(user_data["password"])
                Repository(User).create(user)
