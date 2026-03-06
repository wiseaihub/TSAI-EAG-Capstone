from abc import ABC, abstractmethod

class BaseAgent(ABC):
    name: str
    version: str

    @abstractmethod
    def analyze(self, payload):
        pass
