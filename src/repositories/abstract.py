from abc import ABC, abstractmethod


class KeyValueDBAbstractRepository(ABC):
    @abstractmethod
    async def set(self, key, value):
        pass

    @abstractmethod
    async def delete(self, key):
        pass

    @abstractmethod
    async def get(self, key):
        pass

    @abstractmethod
    async def clear(self):
        pass
