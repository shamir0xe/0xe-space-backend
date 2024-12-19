from __future__ import annotations
from src.database.seeders.user_seeder import UserSeeder


class SeedersOrchestrator:
    def seed_users(self) -> SeedersOrchestrator:
        UserSeeder().seed()
        return self
