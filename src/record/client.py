from typing import Dict, Any
from src.record.base_record import Record


class ClientRecord(Record):
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
        if not self.name:
            raise ValueError("Client name is required.")
        if not self.phone_number:
            raise ValueError("Phone number is required.")

    def to_dict(self) -> Dict[str, Any]:
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