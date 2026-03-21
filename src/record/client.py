from typing import Dict, Any
from src.record.base_record import Record


class ClientRecord(Record):
    """
    Represents a client in the travel record management system.

    A client record stores personal and contact information for
    customers who book flights through the travel agent.

    This class extends the abstract Record class and implements
    the required validation and serialization methods.
    """
    def __init__(
        self,
        name: str,
        address_line_1: str,
        address_line_2: str,
        address_line_3: str,
        city: str,
        state: str,
        zip_code: str,
        country: str,
        phone_number: str,
        record_id: int | None = None
    ) -> None:
        """
        Initialize a new client record.

        The ID may be None when the object is first created.
        The repository assigns the final ID when the record
        is added to the system.
        """
        super().__init__("client")
        self.id = record_id
        self.name = name
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.address_line_3 = address_line_3
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country
        self.phone_number = phone_number

    def validate(self) -> None:
        """
        Validate the structure and required fields of the client record.

        Basic validation ensures that important fields such as
        name and phone number are not empty.
        """
        if not self.name:
            raise ValueError("Client name is required.")
        if not self.phone_number:
            raise ValueError("Phone number is required.")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the client object into a dictionary.

        The repository stores records internally as dictionaries,
        so this method serializes the object into that format.
        """
        return {
            "type": self.type,
            "id": self.id,
            "name": self.name,
            "address_line_1": self.address_line_1,
            "address_line_2": self.address_line_2,
            "address_line_3": self.address_line_3,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "country": self.country,
            "phone_number": self.phone_number,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ClientRecord":
        """
        Create a ClientRecord object from a dictionary.

        This is primarily used when reconstructing objects from
        JSON data loaded from storage.
        """
        return cls(
            name=data["name"],
            address_line_1=data["address_line_1"],
            address_line_2=data["address_line_2"],
            address_line_3=data["address_line_3"],
            city=data["city"],
            state=data["state"],
            zip_code=data["zip_code"],
            country=data["country"],
            phone_number=data["phone_number"],
            record_id=data.get("id"),
        )