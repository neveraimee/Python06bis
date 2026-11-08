from abc import ABC, abstractmethod
from typing import Any, Protocol


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


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class DataStream:
    def __init__(self) -> None:
        self.processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self.processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            handled = False
            for proc in self.processors:
                if proc.validate(element):
                    proc.ingest(element)
                    handled = True
                    break
            if not handled:
                print("DataStream error - Can't process element in "
                      f"stream: {element}")

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self.processors:
            print("No processor found, no data")
            return
        for proc in self.processors:
            name = type(proc).__name__.replace("Processor", " Processor")
            print(f"{name}: total {proc.total} items processed, "
                  f"remaining {len(proc.items)} on processor")

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self.processors:
            data: list[tuple[int, str]] = []
            for _ in range(min(nb, len(proc.items))):
                data.append(proc.output())
            if data:
                plugin.process_output(data)


class CsvExportPlugin:
    @staticmethod
    def quote(text: str) -> str:
        if any(char in text for char in ',"\n'):
            return '"' + text.replace('"', '""') + '"'
        return text

    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("CSV Output:")
        print(",".join(self.quote(text) for _, text in data))


class JsonExportPlugin:
    @staticmethod
    def escape(text: str) -> str:
        return text.replace("\\", "\\\\").replace('"', '\\"')

    def process_output(self, data: list[tuple[int, str]]) -> None:
        pairs = [f'"item_{rank}": "{self.escape(text)}"'
                 for rank, text in data]
        print("JSON Output:")
        print("{" + ", ".join(pairs) + "}")


if __name__ == "__main__":
    print("=== Code Nexus - Data Pipeline ===\n")

    print("Initialize Data Stream...\n")
    stream = DataStream()
    stream.print_processors_stats()

    print("\nRegistering Processors")
    stream.register_processor(NumericProcessor())
    stream.register_processor(TextProcessor())
    stream.register_processor(LogProcessor())

    batch1: list[Any] = [
        "Hello world",
        [3.14, -1, 2.71],
        [{"log_level": "WARNING",
          "log_message": "Telnet access! Use ssh instead"},
         {"log_level": "INFO",
          "log_message": "User wil is connected"}],
        42,
        ["Hi", "five"],
    ]
    print(f"\nSend first batch of data on stream: {batch1}\n")
    stream.process_stream(batch1)
    stream.print_processors_stats()

    print("\nSend 3 processed data from each processor to a CSV plugin:")
    stream.output_pipeline(3, CsvExportPlugin())
    print()
    stream.print_processors_stats()

    batch2: list[Any] = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [{"log_level": "ERROR", "log_message": "500 server crash"},
         {"log_level": "NOTICE",
          "log_message": "Certificate expires in 10 days"}],
        [32, 42, 64, 84, 128, 168],
        "World hello",
    ]
    print(f"\nSend another batch of data: {batch2}\n")
    stream.process_stream(batch2)
    stream.print_processors_stats()

    print("\nSend 5 processed data from each processor to a JSON plugin:")
    stream.output_pipeline(5, JsonExportPlugin())
    print()
    stream.print_processors_stats()