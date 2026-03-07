from abc import ABC, abstractmethod
from typing import Dict, Any


class Record(ABC):
    def __init__(self, record_type: str) -> None:
        self.type = record_type

    @abstractmethod
    def validate(self) -> None:
        """Validate record structure."""

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Record":       
        """Create record object from dictionary."""