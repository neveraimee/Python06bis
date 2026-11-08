from abc import ABC, abstractmethod
from typing import Any

class DataProcessor(ABC):
    def __init__(self) -> None:
        self.items: list[str] = []
        self.total: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self.items:
            raise IndexError("No data to output")
        rank = self.total - len(self.items)
        return (rank, self.items.pop(0))


class NumericProcessor(DataProcessor):
    @staticmethod
    def is_number(value: Any) -> bool:
        return (isinstance(value, (int, float))
                and not isinstance(value, bool))

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(self.is_number(item) for item in data)
        return self.is_number(data)

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        values = data if isinstance(data, list) else [data]
        for value in values:
            self.items.append(str(value))
            self.total += 1


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(isinstance(item, str) for item in data)
        return isinstance(data, str)

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        texts = data if isinstance(data, list) else [data]
        for text in texts:
            self.items.append(text)
            self.total += 1


class LogProcessor(DataProcessor):
    @staticmethod
    def is_log(entry: Any) -> bool:
        if not isinstance(entry, dict):
            return False
        for key, value in entry.items():
            if not isinstance(key, str) or not isinstance(value, str):
                return False
        return "log_level" in entry and "log_message" in entry

    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            return all(self.is_log(entry) for entry in data)
        return self.is_log(data)

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        entries = data if isinstance(data, list) else [data]
        for entry in entries:
            self.items.append(f"{entry['log_level']}: {entry['log_message']}")
            self.total += 1


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===\n")

    print("Testing Numeric Processor...")
    num = NumericProcessor()
    print(f" Trying to validate input '42': {num.validate(42)}")
    print(f" Trying to validate input 'Hello': {num.validate('Hello')}")
    print(" Test invalid ingestion of string 'foo' without prior "
          "validation:")
    try:
        num.ingest("foo")
    except ValueError as error:
        print(f" Got exception: {error}")
    numbers: list[int | float] = [1, 2, 3, 4, 5]
    print(f" Processing data: {numbers}")
    num.ingest(numbers)
    print(" Extracting 3 values...")
    for _ in range(3):
        rank, value = num.output()
        print(f" Numeric value {rank}: {value}")

    print("\nTesting Text Processor...")
