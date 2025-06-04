from typing import Protocol, Any


class PropertyChangedListenerProtocol(Protocol):
    def on_property_changed(self, obj: Any, property_name: str) -> None: ...


class DataChangedProtocol(Protocol):
    def add_property_changed_listener(
        self, listener: PropertyChangedListenerProtocol
    ) -> None: ...
    def remove_property_changed_listener(
        self, listener: PropertyChangedListenerProtocol
    ) -> None: ...


class PropertyChangingListenerProtocol(Protocol):
    def on_property_changing(
        self, obj: Any, property_name: str, old_value: Any, new_value: Any
    ) -> bool: ...


class DataChangingProtocol(Protocol):
    def add_property_changing_listener(
        self, listener: PropertyChangingListenerProtocol
    ) -> None: ...
    def remove_property_changing_listener(
        self, listener: PropertyChangingListenerProtocol
    ) -> None: ...


class Person(DataChangedProtocol, DataChangingProtocol):
    def __init__(self, name: str, age: int):
        self._name = name
        self._age = age
        self._change_listeners: set[PropertyChangedListenerProtocol] = set()
        self._changing_listeners: set[PropertyChangingListenerProtocol] = set()

    def add_property_changed_listener(
        self, listener: PropertyChangedListenerProtocol
    ) -> None:
        self._change_listeners.add(listener)

    def remove_property_changed_listener(
        self, listener: PropertyChangedListenerProtocol
    ) -> None:
        self._change_listeners.discard(listener)

    def add_property_changing_listener(
        self, listener: PropertyChangingListenerProtocol
    ) -> None:
        self._changing_listeners.add(listener)

    def remove_property_changing_listener(
        self, listener: PropertyChangingListenerProtocol
    ) -> None:
        self._changing_listeners.discard(listener)

    def _notify_property_changing(
        self, property_name: str, old_value: Any, new_value: Any
    ) -> bool:
        for listener in self._changing_listeners:
            if not listener.on_property_changing(
                self, property_name, old_value, new_value
            ):
                return False
        return True

    def _notify_property_changed(self, property_name: str) -> None:
        for listener in self._change_listeners:
            listener.on_property_changed(self, property_name)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if value != self._name and self._notify_property_changing(
            "name", self._name, value
        ):
            self._name = value
            self._notify_property_changed("name")

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        if value != self._age and self._notify_property_changing(
            "age", self._age, value
        ):
            self._age = value
            self._notify_property_changed("age")


class PrintChangeListener(PropertyChangedListenerProtocol):
    def on_property_changed(self, obj: Any, property_name: str) -> None:
        print(f"[Изменено] {property_name}: {getattr(obj, property_name)}")


class AgeValidator(PropertyChangingListenerProtocol):
    def on_property_changing(
        self, obj: Any, property_name: str, old_value: Any, new_value: Any
    ) -> bool:
        if property_name == "age" and (new_value < 0 or new_value > 150):
            print(f"[Ошибка] Недопустимый возраст: {new_value}")
            return False
        return True


class NameValidator(PropertyChangingListenerProtocol):
    def on_property_changing(
        self, obj: Any, property_name: str, old_value: Any, new_value: Any
    ) -> bool:
        if property_name == "name" and not new_value.strip():
            print("[Ошибка] Имя не может быть пустым.")
            return False
        return True


if __name__ == "__main__":
    user = Person("Иван", 25)
    print(f"[Исходное] name: {user.name}")
    print(f"[Исходное] age: {user.age}")

    user.add_property_changed_listener(PrintChangeListener())
    user.add_property_changing_listener(AgeValidator())
    user.add_property_changing_listener(NameValidator())

    user.name = "Алексей"  # OK
    user.name = ""  # Error
    user.age = 170  # Error
    user.age = 30  # OK
