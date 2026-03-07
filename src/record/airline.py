from typing import Dict, Any
from src.record.base_record import Record


class AirlineRecord(Record):
    """
    Represents an airline company in the system.

    Airline records store the company name and a unique ID.
    Flights reference airlines using their ID.
    """
    def __init__(
        self,
        company_name: str,
        record_id: int | None = None
    ) -> None:
        """
        Initialize an airline record.

        The repository assigns the final ID when the airline
        is added to the system.
        """
        super().__init__("airline")
        self.id = record_id
        self.company_name = company_name

    def validate(self) -> None:
        """
        Validate the airline record.

        Ensures the company name is not empty.
        """
        if not self.company_name:
            raise ValueError("Company name is required.")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the airline object into a dictionary for storage.
        """
        return {
            "type": self.type,
            "id": self.id,
            "company_name": self.company_name,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AirlineRecord":
        """
        Recreate an AirlineRecord object from stored dictionary data.
        """
        return cls(
            company_name=data["company_name"],
            record_id=data.get("id"),
        )