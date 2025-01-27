from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class BaseFactory(ABC, Generic[T]):

    @abstractmethod
    def create(self, *args, **kwargs) -> T:
        pass
