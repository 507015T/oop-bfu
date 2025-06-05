from injector import Injector
from interfaces import IServiceA, IServiceB, IServiceC
from lifecycle import LifeStyle
from services import (
    ServiceADebug,
    ServiceBDebug,
    ServiceCDebug,
    ServiceARelease,
    ServiceBRelease,
    ServiceCRelease,
)

# ===== Configuration 1 =====
config1 = Injector()
config1.register(IServiceA, ServiceADebug, LifeStyle.PER_REQUEST)
config1.register(IServiceB, ServiceBDebug, LifeStyle.SCOPED)
config1.register(IServiceC, ServiceCDebug, LifeStyle.SINGLETON)

# ===== Configuration 2 =====
config2 = Injector()
config2.register(IServiceA, ServiceARelease, LifeStyle.SINGLETON)
config2.register(IServiceB, ServiceBRelease, LifeStyle.PER_REQUEST)
config2.register(
    IServiceC,
    lambda: ServiceCRelease(config2.get_instance(IServiceB)),
    LifeStyle.PER_REQUEST,
)
