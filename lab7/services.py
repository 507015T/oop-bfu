from interfaces import IServiceA, IServiceB, IServiceC


class ServiceADebug(IServiceA):
    def do_a(self) -> str:
        return "A debug"


class ServiceARelease(IServiceA):
    def do_a(self) -> str:
        return "A release"


class ServiceBDebug(IServiceB):
    def __init__(self, a_service: IServiceA):
        self._a = a_service

    def do_b(self) -> str:
        return f"B debug uses {self._a.do_a()}"


class ServiceBRelease(IServiceB):
    def __init__(self, a_service: IServiceA):
        self._a = a_service

    def do_b(self) -> str:
        return f"B release uses {self._a.do_a()}"


class ServiceCDebug(IServiceC):
    def __init__(self, b_service: IServiceB):
        self._b = b_service

    def do_c(self) -> str:
        return f"C debug uses {self._b.do_b()}"


class ServiceCRelease(IServiceC):
    def __init__(self, b_service: IServiceB):
        self._b = b_service

    def do_c(self) -> str:
        return f"C release uses {self._b.do_b()}"
