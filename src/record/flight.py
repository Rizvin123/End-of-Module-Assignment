from typing import Dict, Any
from datetime import datetime
from src.record.base_record import Record


class FlightRecord(Record):
    """
    Represents a flight booking in the system.

    A flight connects a client with an airline and contains
    travel information such as date and route.
    """
    def __init__(
        self,
        client_id: int,
        airline_id: int,
        date: datetime,
        start_city: str,
        end_city: str,
    ) -> None:
        """
        Initialize a flight record.

        The client_id and airline_id act as foreign keys,
        linking the flight to existing client and airline records.
        """
        super().__init__("flight")
        self.client_id = client_id
        self.airline_id = airline_id
        self.date = date
        self.start_city = start_city
        self.end_city = end_city

    def validate(self) -> None:
        """
        Validate the flight data.

        Ensures that required fields such as route information
        and foreign key references are present.
        """
        if not isinstance(self.client_id, int):
            raise ValueError("Client ID must be an integer.")
        if not isinstance(self.airline_id, int):
            raise ValueError("Airline ID must be an integer.")
        if not isinstance(self.date, datetime):
            raise ValueError("Date must be a datetime object.")
        if not self.start_city:
            raise ValueError("Start city is required.")
        if not self.end_city:
            raise ValueError("End city is required.")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the flight object into a dictionary.

        The date is converted to ISO format so it can be safely
        stored in JSON format.
        """
        return {
            "type": self.type,
            "client_id": self.client_id,
            "airline_id": self.airline_id,
            "date": self.date.isoformat(),
            "start_city": self.start_city,
            "end_city": self.end_city,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FlightRecord":
        """
        Reconstruct a FlightRecord object from stored dictionary data.
        """
        return cls(
            client_id=data["client_id"],
            airline_id=data["airline_id"],
            date=datetime.fromisoformat(data["date"]),
            start_city=data["start_city"],
            end_city=data["end_city"],
        )