import pytest
from datetime import datetime
from src.record.client import ClientRecord
from src.record.airline import AirlineRecord
from src.record.flight import FlightRecord


def test_valid_client():
    """
    Test that a valid ClientRecord passes validation.

    This verifies that when all required fields are provided,
    the validate() method does not raise any errors.
    """
    client = ClientRecord(
        name="John",
        address_line_1="A",
        address_line_2="B",
        address_line_3="C",
        city="Lucknow",
        state="UP",
        zip_code="226001",
        country="India",
        phone_number="1234567890"
    )
    client.validate()


def test_client_missing_name_raises():
    """
    Test that validation fails when the client name is missing.

    The ClientRecord validation rules require a non-empty name.
    This test confirms that validate() raises a ValueError
    when the name field is empty.
    """
    client = ClientRecord(
        name="",
        address_line_1="A",
        address_line_2="B",
        address_line_3="C",
        city="Lucknow",
        state="UP",
        zip_code="226001",
        country="India",
        phone_number="1234567890"
    )
    with pytest.raises(ValueError):
        client.validate()


def test_flight_round_trip():
    """
    Test serialization and deserialization of a FlightRecord.

    This test ensures that:
    1. A FlightRecord can be converted to a dictionary using to_dict()
    2. The dictionary can be converted back into a FlightRecord using from_dict()
    3. The reconstructed object contains the same values as the original

    This confirms that the model supports correct persistence and reconstruction.
    """
    date = datetime.now()
    flight = FlightRecord(1, 2, date, "Delhi", "Dubai")
    data = flight.to_dict()
    restored = FlightRecord.from_dict(data)

    assert restored.client_id == 1
    assert restored.airline_id == 2
    assert restored.date == date
    assert restored.start_city == "Delhi"
    assert restored.end_city == "Dubai"

def test_valid_airline():
    """
    Test that a valid AirlineRecord passes validation.

    If the company name is provided, validate() should complete
    without raising any errors.
    """
    airline = AirlineRecord("Emirates")
    airline.validate()


def test_airline_missing_name_raises():
    """
    Test that a valid AirlineRecord passes validation.

    If the company name is provided, validate() should complete
    without raising any errors.
    """
    airline = AirlineRecord("")
    with pytest.raises(ValueError):
        airline.validate()

def test_flight_missing_start_city_raises():
    """
    Test that a flight with an empty start city fails validation.

    Flights must include both start_city and end_city.
    This test confirms that validate() raises a ValueError
    when the start city is missing.
    """
    flight = FlightRecord(
        client_id=1,
        airline_id=2,
        date=datetime.now(),
        start_city="",
        end_city="Dubai"
    )

    with pytest.raises(ValueError):
        flight.validate()

def test_client_to_dict_contains_required_fields():
    """
    Test that converting a client to a dictionary includes
    all required fields used by the repository and storage layers.
    """
    client = ClientRecord(
        name="Alice",
        address_line_1="A",
        address_line_2="B",
        address_line_3="C",
        city="Delhi",
        state="DL",
        zip_code="110001",
        country="India",
        phone_number="9876543210"
    )

    data = client.to_dict()

    assert data["type"] == "client"
    assert data["name"] == "Alice"
    assert data["city"] == "Delhi"
    assert data["phone_number"] == "9876543210"

def test_airline_round_trip():
    """
    Test that an airline can be converted to a dictionary
    and reconstructed back into an AirlineRecord.
    """
    airline = AirlineRecord("Qatar Airways")
    data = airline.to_dict()

    restored = AirlineRecord.from_dict(data)

    assert restored.company_name == "Qatar Airways"