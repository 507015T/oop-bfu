from typing import Protocol, List
import re
import sys
from datetime import datetime
import aiofiles
import asyncio


class LogFilterProtocol(Protocol):
    def match(self, text: str) -> bool: ...


class SimpleLogFilter(LogFilterProtocol):
    def __init__(self, pattern: str) -> None:
        self.pattern = pattern

    def match(self, text: str) -> bool:
        return self.pattern in text


class ReLogFilter(LogFilterProtocol):
    def __init__(self, pattern: str) -> None:
        self.regex = re.compile(pattern)

    def match(self, text: str) -> bool:
        return bool(self.regex.search(text))


class LevelFilter(LogFilterProtocol):
    def __init__(self, level: str) -> None:
        self.level = level.upper()

    def match(self, text: str) -> bool:
        return text.startswith(self.level)


class LogHandlerProtocol(Protocol):
    async def handle(self, text: str) -> None: ...


class FileHandler(LogHandlerProtocol):
    def __init__(self, filename: str) -> None:
        self.filename = filename

    async def handle(self, text: str) -> None:
        try:
            await self._handle(text)
        except (IOError, PermissionError) as e:
            sys.stderr.write(f"FileHandler error: {e}\n")
        except Exception as e:
            sys.stderr.write(f"FileHandler unexpected error: {e}\n")

    async def _handle(self, text: str) -> None:
        async with aiofiles.open(self.filename, "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await f.write(f"[{timestamp}] {text}\n")


class SocketHandler(LogHandlerProtocol):
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

    async def handle(self, text: str) -> None:
        try:
            await self._handle(text)
        except (OSError, asyncio.TimeoutError) as e:
            sys.stderr.write(f"SocketHandler error: {e}\n")
        except Exception as e:
            sys.stderr.write(f"SocketHandler unexpected error: {e}\n")

    async def _handle(self, text: str) -> None:
        _, writer = await asyncio.wait_for(
            asyncio.open_connection(self.host, self.port), timeout=1.0
        )
        writer.write((text + "\n").encode("utf-8"))
        await writer.drain()
        writer.close()
        await writer.wait_closed()


class ConsoleHandler(LogHandlerProtocol):
    def __init__(self, use_stderr: bool = False) -> None:
        self.use_stderr = use_stderr

    async def handle(self, text: str) -> None:
        try:
            if self.use_stderr:
                sys.stderr.write(f"{text}\n")
            else:
                print(text)
        except Exception as e:
            sys.stderr.write(f"ConsoleHandler error: {e}\n")


class SyslogHandler(LogHandlerProtocol):
    async def handle(self, text: str) -> None:
        try:
            sys.stderr.write(f"SYSLOG: {text}\n")
        except Exception as e:
            sys.stderr.write(f"SyslogHandler error: {e}\n")


class Logger:
    def __init__(
        self, filters: List[LogFilterProtocol], handlers: List[LogHandlerProtocol]
    ) -> None:
        self._filters = filters
        self._handlers = handlers

    async def log(self, text: str) -> None:
        if all(f.match(text) for f in self._filters):
            for handler in self._handlers:
                try:
                    await handler.handle(text)
                except Exception as e:
                    sys.stderr.write(f"Logger failed to handle log: {e}\n")


async def main() -> None:
    print("Демонстрация работы асинхронной системы логирования")

    error_filter = SimpleLogFilter("ERROR")
    warning_filter = SimpleLogFilter("WARNING")
    digit_filter = ReLogFilter(r"\d+")
    level_filter = LevelFilter("INFO")

    console_handler = ConsoleHandler()
    error_file_handler = FileHandler("error_logs.txt")
    all_file_handler = FileHandler("all_logs.txt")
    syslog_handler = SyslogHandler()

    print("\nПример 1: ERROR логи с цифрами")
    logger1 = Logger(
        [error_filter, digit_filter], [console_handler, error_file_handler]
    )
    await logger1.log("ERROR: Код ошибки 503")
    await logger1.log("WARNING: Замечено нестабильное поведение")
    await logger1.log("ERROR: Ошибка 500 при обращении к API")

    print("\nПример 2: INFO логи")
    logger2 = Logger([level_filter], [all_file_handler, syslog_handler])
    await logger2.log("INFO: Инициализация завершена успешно")
    await logger2.log("INFO: Установлено соединение с базой данных")
    await logger2.log("WARNING: Скорость ответа сервиса снизилась")

    print("\nПример 3: WARNING логи")
    logger3 = Logger([warning_filter], [console_handler])
    await logger3.log("WARNING: Используется устаревший протокол")
    await logger3.log("ERROR: Критическая ошибка ядра")  # это не попадёт

    print("\nПример 4: Все логи")
    logger4 = Logger([], [console_handler])
    await logger4.log("DEBUG: Получены входные параметры от клиента")
    await logger4.log("INFO: Выполнена очистка кэша")
    await logger4.log("ERROR: Не удалось сохранить файл")
    await logger4.log("WARNING: Память на сервере почти заполнена")


if __name__ == "__main__":
    asyncio.run(main())
