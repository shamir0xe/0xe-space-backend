from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseValidator(ABC):

    @abstractmethod
    def validate(self) -> bool:
        pass
