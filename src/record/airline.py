from typing import Dict, Any
from src.record.base_record import Record


class AirlineRecord(Record):
    def __init__(
        self,
        company_name: str,
        record_id: int | None = None
    ) -> None:
        super().__init__("airline")
        self.id = record_id
        self.company_name = company_name

    def validate(self) -> None:
        if not self.company_name:
            raise ValueError("Company name is required.")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "id": self.id,
            "company_name": self.company_name,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AirlineRecord":
        return cls(
            company_name=data["company_name"],
            record_id=data.get("id"),
        )