import json
from pathlib import Path
from typing import List, Dict, Any


class JsonStorage:
    """
    Storage layer responsible for persisting records to disk.

    This class isolates file handling from the rest of the system.
    The repository manages business logic and passes data to this
    class when records need to be saved or loaded.
    """
    def __init__(self, file_path: str | Path) -> None:
        """
        Initialize storage with the path to the JSON file.

        The path is converted to a Path object so we can use
        convenient file system operations from pathlib.
        """
        self.file_path = Path(file_path)

    def exists(self) -> bool:
        """
        Check whether the data file exists.

        Used by the repository during startup to determine
        whether it should load existing records or start
        with an empty dataset.
        """
        return self.file_path.exists()

    def load(self) -> List[Dict[str, Any]]:
        """
        Load records from the JSON file.

        If the file does not exist, an empty list is returned.
        Otherwise the JSON file is parsed and converted into
        a list of dictionaries representing records.
        """
        if not self.exists():
            return []

        with self.file_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, records: List[Dict[str, Any]]) -> None:
        """
        Save all records to the JSON file.

        A temporary file is used to ensure safe writes.
        This prevents data corruption if the application
        crashes during the save operation.

        Steps:
        1. Write data to a temporary file
        2. Replace the original file with the temporary file
        """
        temp_path = self.file_path.with_suffix(".tmp")

        with temp_path.open("w", encoding="utf-8") as f:
            json.dump(records, f, indent=4)

        temp_path.replace(self.file_path)