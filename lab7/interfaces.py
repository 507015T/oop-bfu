from abc import ABC, abstractmethod


class IServiceA(ABC):
    @abstractmethod
    def do_a(self) -> str:
        pass


class IServiceB(ABC):
    @abstractmethod
    def do_b(self) -> str:
        pass


class IServiceC(ABC):
    @abstractmethod
    def do_c(self) -> str:
        pass
