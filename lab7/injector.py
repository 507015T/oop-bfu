from lifecycle import LifeStyle
from contextlib import contextmanager
from inspect import signature, isclass
from typing import Type, Any, Optional, Callable, Union


class Injector:
    _registry: dict[Type, tuple[Union[Type, Callable], LifeStyle, dict]]
    _singletons: dict[Type, Any]

    def __init__(self):
        self._registry = {}
        self._singletons = {}
        self._scoped_instances: Optional[dict[Type, Any]] = None

    def register(
        self,
        interface: Type,
        implementation: Union[Type, Callable],
        lifestyle: LifeStyle = LifeStyle.PER_REQUEST,
        params: Optional[dict] = None,
    ):
        self._registry[interface] = (implementation, lifestyle, params or {})

    def get_instance(self, interface: Type) -> Any:
        impl, lifestyle, params = self._registry[interface]

        if lifestyle == LifeStyle.SINGLETON:
            if interface not in self._singletons:
                self._singletons[interface] = self._build(impl, params)
            return self._singletons[interface]

        if lifestyle == LifeStyle.SCOPED:
            if self._scoped_instances is None:
                raise RuntimeError("No active scope")
            if interface not in self._scoped_instances:
                self._scoped_instances[interface] = self._build(impl, params)
            return self._scoped_instances[interface]

        return self._build(impl, params)

    def _build(self, impl: Union[Type, Callable], params: dict) -> Any:
        if callable(impl) and not isclass(impl):
            return impl()

        ctor_params = {}
        sig = signature(impl.__init__)
        for name, param in sig.parameters.items():
            if param.annotation in self._registry:
                ctor_params[name] = self.get_instance(param.annotation)
        ctor_params.update(params)
        return impl(**ctor_params)

    @contextmanager
    def create_scope(self):
        previous = self._scoped_instances
        self._scoped_instances = {}
        try:
            yield
        finally:
            self._scoped_instances = previous
