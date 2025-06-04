import json
import os
from enum import Enum
from typing import Self, Tuple, List

FONT_FILE = "font.json"


class Color(Enum):
    RED = "\033[31m"
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    MAGENTA = "\033[35m"
    RESET = "\033[0m"


if not os.path.exists(FONT_FILE):
    raise FileNotFoundError(FONT_FILE)

with open(FONT_FILE, "r", encoding="utf-8") as f:
    FONT_DATA = json.load(f)


class Printer:
    def __init__(
        self,
        color: Color,
        position: Tuple[int, int] = (0, 0),
        symbol: str = "*",
        font_size: int = 1,
    ) -> None:
        self.color = color
        self.position = position
        self.symbol = symbol
        self.font_size = font_size

    def print_text(self, text: str) -> None:
        self.__class__.print(
            text, self.color, self.position, self.symbol, self.font_size
        )

    @classmethod
    def print(
        cls,
        text: str,
        color: Color,
        position: Tuple[int, int] = (0, 0),
        symbol: str = "*",
        font_size: int = 1,
    ) -> None:
        cls._render_text(text, color, position, symbol, font_size)

    @classmethod
    def _render_text(
        cls,
        text: str,
        color: Color,
        position: Tuple[int, int],
        symbol: str,
        font_size: int,
    ) -> None:
        base_height = FONT_DATA["height"]
        lines = ["" for _ in range(base_height * font_size)]

        for char in text.upper():
            if char not in FONT_DATA["symbols"]:
                continue
            char_pattern = FONT_DATA["symbols"][char].split("\n")
            scaled_pattern = cls._scale_pattern(char_pattern, font_size)

            for i, line in enumerate(scaled_pattern):
                if symbol:
                    line = line.replace("*", symbol)
                lines[i] += line + (" " * font_size * 2)

        print(color.value, end="\n")
        for i, line in enumerate(lines):
            y = position[1] + i
            x = position[0]
            print(f"\033[{y};{x}H{line}")
        print(Color.RESET.value, end="")

    @staticmethod
    def _scale_pattern(pattern: List[str], scale: int) -> List[str]:
        if scale == 1:
            return pattern

        scaled_pattern = []
        for line in pattern:
            scaled_line = "".join(char * scale for char in line)
            for _ in range(scale):
                scaled_pattern.append(scaled_line)
        return scaled_pattern

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        print(Color.RESET.value, end="")


if __name__ == "__main__":

    Printer.print("SMALL", Color.RED, (5, 40), "●", 1)
    Printer.print("MEDIUM", Color.GREEN, (10, 40), "▲", 2)
    Printer.print("LARGE", Color.BLUE, (11, 40), "♦", 3)
    with Printer(Color.CYAN, (5, 40), "♥", 1) as small_printer:
        small_printer.print_text("LOVE")

    with Printer(Color.MAGENTA, (10, 40), "♣", 2) as medium_printer:
        medium_printer.print_text("LOVE")

    with Printer(Color.YELLOW, (15, 40), "■", 3) as large_printer:
        large_printer.print_text("LOVE")
