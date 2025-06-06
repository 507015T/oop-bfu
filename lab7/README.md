## Лабораторная работа 7 (внедреж зависимостей)

**Написать сервис, который управляет управляет ассоциациями между интерфейсами и классами их реализующими. См. Dependency Injection (Рзавитие концециии фабрики классов)**

1. Создать класс инжектор должен поддерживать

- 3 различных режима жизненного цикла соаздаваемы классов LifeStyle: PerRequest, Scoped, Singleton
- регистрацию зависимости между интерфейсов и классом
  напр: register(self, interface_type, class_type, life_circle)
- возможность передачи дополнительных параметров в конструктор регистрируемого класса
  напр: register(self, interface_type, class_type, life_circle, params)
- используовние в конструкторе регистрируемого интерфейса другие уже зарегистрированные интерфейсы
- метод для возвращаения экземпляра класса по интерфейсу.
  напр: get_instance(self, interface_type) -> class_instance
- В зависимости от ассоциированого LifeStyle get_instance должен работать по-разному:
  PerRequest => возвращает каждй раз новый экзепляр класса
  Scoped => возврващет один и тот же экземпляр внутри Scope (внутри открытой области). Можно реализвать, например через with в python
  Singleton => всегда возвращает один и тот же экзмепляр объекта
- добавить также возможность акссоциации интерфейса с фабричным методом, возваращающим класс
  напр: register(self, interface_type, fabric_method)

2. Создать минимум три интерфейса
   напр: interface1, interface2, interface3
   Под каждый интерфейс создать минимум два класса его поддерживающего с разными LifeCircle
   напр: class1_debug(interface1), class1_release(interface1), class2_debug(interface2), class2_release(interface2), class3_debug(interface3), class3_release(interface3)

3. Создать две конфигурации c различными регистрациями реализаций interface1, interface2, interface3

4. Продемнстировать получение экземпляров классов при помощи инжектора и их дальнейшее использование
