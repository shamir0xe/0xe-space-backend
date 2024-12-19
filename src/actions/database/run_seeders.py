from src.orchestrators.seeders_orchestrator import SeedersOrchestrator


class RunSeeders:
    @staticmethod
    def run() -> None:
        SeedersOrchestrator().seed_users()
