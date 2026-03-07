import json
from pathlib import Path
from typing import List, Dict, Any


class JsonStorage:
    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)

    def exists(self) -> bool:
        return self.file_path.exists()

    def load(self) -> List[Dict[str, Any]]:
        if not self.exists():
            return []

        with self.file_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, records: List[Dict[str, Any]]) -> None:
        temp_path = self.file_path.with_suffix(".tmp")

        with temp_path.open("w", encoding="utf-8") as f:
            json.dump(records, f, indent=4)

        temp_path.replace(self.file_path)