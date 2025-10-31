from abc import ABC, abstractmethod
from typing import Dict, Generic, TypeVar, List, Optional

T = TypeVar("T")  # Entity type

class IRepository(ABC, Generic[T]):
    @abstractmethod
    def add(self, entity: T) -> T:
        pass

    @abstractmethod
    def get(self, entity_id: int) -> Optional[T]:
        pass

    @abstractmethod
    def list(self) -> List[T]:
        pass

    @abstractmethod
    def update(self, entity_id: int, entity: T) -> T:
        pass

    @abstractmethod
    def delete(self, entity_id: int) -> None:
        pass


class InMemoryDictRepository(IRepository[T], Generic[T]):
    def __init__(self):
        self._store: Dict[int, T] = {}
        self._counter = 1

    def add(self, entity: T) -> T:
        entity_id = getattr(entity, "id", None) or self._counter
        setattr(entity, "id", entity_id)
        self._store[entity_id] = entity
        self._counter += 1
        return entity

    def get(self, entity_id: int) -> Optional[T]:
        return self._store.get(entity_id)

    def list(self) -> List[T]:
        return list(self._store.values())

    def update(self, entity_id: int, entity: T) -> T:
        if entity_id not in self._store:
            raise ValueError(f"Entity {entity_id} not found")
        self._store[entity_id] = entity
        return entity

    def delete(self, entity_id: int) -> None:
        self._store.pop(entity_id, None)


