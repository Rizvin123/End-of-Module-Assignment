from abc import ABC, abstractmethod
from typing import Dict, Any


class Record(ABC):
    """
    Abstract base class for all record types in the system.

    This class defines the common structure and behavior that
    every record must implement (Client, Airline, Flight).

    Using an abstract base class ensures consistency across all
    record types and allows the repository to work with records
    in a uniform way.
    """
    def __init__(self, record_type: str) -> None:
        """
        Initialize the record with a type identifier.

        The 'type' field is used throughout the system to distinguish
        between different record categories such as:
        - client
        - airline
        - flight

        This allows all records to be stored in a single unified list.
        """
        self.type = record_type

    @abstractmethod
    def validate(self) -> None:
        """
        Validate the record's data.

        Each subclass must implement its own validation rules.
        For example:
        - ClientRecord checks name, address, phone number
        - AirlineRecord checks company name
        - FlightRecord checks client_id, airline_id, dates, etc.

        If validation fails, a ValueError should be raised.
        """

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the record object into a dictionary representation.

        The repository stores records internally as dictionaries,
        so every record must provide a method to serialize itself
        into a dictionary format suitable for storage or JSON export.
        """

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Record":       
        """
        Create a record object from a dictionary.

        This method performs the reverse operation of to_dict().
        It allows the system to reconstruct record objects when
        loading data from JSON storage.
        """