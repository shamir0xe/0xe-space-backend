from abc import ABC, abstractmethod


class BaseSeeder(ABC):
    @abstractmethod
    def seed(self) -> None:
        pass
