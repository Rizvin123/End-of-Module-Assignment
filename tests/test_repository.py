from src.data.storage import JsonStorage
from src.data.repository import RecordRepository
from src.record.client import ClientRecord
from src.record.airline import AirlineRecord
from src.record.flight import FlightRecord
from datetime import datetime
import pytest


def test_repository_initializes_empty(tmp_path):
    """
    Test that a newly created repository starts with no records.

    This verifies that when no storage file exists, the repository
    initializes correctly with an empty list and the ID counters
    start at 1 for clients and airlines.
    """
    storage = JsonStorage(tmp_path / "records.json")
    repo = RecordRepository(storage)

    assert repo.records == []
    assert repo.next_client_id == 1
    assert repo.next_airline_id == 1


def test_create_client_assigns_id(tmp_path):
    """
    Test that creating a client assigns a unique ID.

    This verifies that:
    - A new client is added to the repository
    - The client receives ID = 1
    - The next_client_id counter increments correctly.
    """
    storage = JsonStorage(tmp_path / "records.json")
    repo = RecordRepository(storage)

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

    repo.create_client(client)

    assert len(repo.records) == 1
    assert repo.records[0]["id"] == 1
    assert repo.next_client_id == 2

def test_multiple_clients_increment_ids(tmp_path):
    """
    Test that multiple client creations produce sequential IDs.

    This ensures the repository correctly increments the
    client ID counter when several clients are created.
    """
    storage = JsonStorage(tmp_path / "records.json")
    repo = RecordRepository(storage)

    for i in range(3):
        client = ClientRecord(
            name=f"Client{i}",
            address_line_1="A",
            address_line_2="B",
            address_line_3="C",
            city="Lucknow",
            state="UP",
            zip_code="226001",
            country="India",
            phone_number="1234567890"
        )
        repo.create_client(client)

    assert repo.records[2]["id"] == 3
    assert repo.next_client_id == 4


def test_create_airline_assigns_id(tmp_path):
    """
    Test that creating an airline assigns a unique ID.

    Confirms that:
    - The airline record is stored correctly
    - The correct type field is set
    - The airline ID counter increments.
    """
    storage = JsonStorage(tmp_path / "records.json")
    repo = RecordRepository(storage)

    airline = AirlineRecord("Emirates")
    repo.create_airline(airline)

    assert len(repo.records) == 1
    assert repo.records[0]["id"] == 1
    assert repo.records[0]["type"] == "airline"
    assert repo.next_airline_id == 2

def test_create_flight_with_valid_references(tmp_path):
    """
    Test creating a flight when both client and airline exist.

    This verifies that the repository correctly allows a flight
    to be created when the referenced client_id and airline_id
    are valid.
    """
    storage = JsonStorage(tmp_path / "records.json")
    repo = RecordRepository(storage)

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
    repo.create_client(client)

    airline = AirlineRecord("Emirates")
    repo.create_airline(airline)

    flight = FlightRecord(
        client_id=1,
        airline_id=1,
        date=datetime.now(),
        start_city="Delhi",
        end_city="Dubai"
    )

    repo.create_flight(flight)
    assert len(repo.records) == 3
    assert repo.records[-1]["type"] == "flight"

def test_create_flight_invalid_client_raises(tmp_path):
    """
    Test that creating a flight with a non-existent client fails.

    The repository should enforce referential integrity and
    raise a ValueError if the referenced client does not exist.
    """
    storage = JsonStorage(tmp_path / "records.json")
    repo = RecordRepository(storage)

    airline = AirlineRecord("Emirates")
    repo.create_airline(airline)

    flight = FlightRecord(
        client_id=999,
        airline_id=1,
        date=datetime.now(),
        start_city="Delhi",
        end_city="Dubai"
    )

    with pytest.raises(ValueError):
        repo.create_flight(flight)

def test_delete_client_without_flights(tmp_path):
    """
    Test deleting a client that has no associated flights.

    This confirms that the repository allows deletion
    when no flight records reference the client.
    """
    storage = JsonStorage(tmp_path / "records.json")
    repo = RecordRepository(storage)

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
    repo.create_client(client)

    repo.delete_client(1)

    assert len(repo.records) == 0

def test_delete_client_with_flights_raises(tmp_path):
    """
    Test that a client cannot be deleted if flights reference it.

    This verifies that the repository enforces referential integrity
    and prevents deletion of records that are still referenced.
    """
    storage = JsonStorage(tmp_path / "records.json")
    repo = RecordRepository(storage)

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
    repo.create_client(client)

    airline = AirlineRecord("Emirates")
    repo.create_airline(airline)

    flight = FlightRecord(
        client_id=1,
        airline_id=1,
        date=datetime.now(),
        start_city="Delhi",
        end_city="Dubai"
    )
    repo.create_flight(flight)

    with pytest.raises(ValueError):
        repo.delete_client(1)

def test_delete_airline_without_flights(tmp_path):
    """
    Test deleting an airline that is not referenced by any flights.

    The repository should allow deletion when there are
    no dependent flight records.
    """
    storage = JsonStorage(tmp_path / "records.json")
    repo = RecordRepository(storage)

    airline = AirlineRecord("Emirates")
    repo.create_airline(airline)

    repo.delete_airline(1)

    assert len(repo.records) == 0

def test_delete_airline_with_flights_raises(tmp_path):
    """
    Test that an airline cannot be deleted if flights reference it.

    This ensures the repository prevents orphaned flight records.
    """
    storage = JsonStorage(tmp_path / "records.json")
    repo = RecordRepository(storage)

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
    repo.create_client(client)

    airline = AirlineRecord("Emirates")
    repo.create_airline(airline)

    flight = FlightRecord(
        client_id=1,
        airline_id=1,
        date=datetime.now(),
        start_city="Delhi",
        end_city="Dubai"
    )
    repo.create_flight(flight)

    with pytest.raises(ValueError):
        repo.delete_airline(1)

def test_update_client_valid(tmp_path):
    """
    Test updating a client with valid data.

    Confirms that the repository correctly modifies the
    client record when the update passes validation.
    """
    storage = JsonStorage(tmp_path / "records.json")
    repo = RecordRepository(storage)

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
    repo.create_client(client)

    repo.update_client(1, {"city": "Delhi"})

    updated = repo.records[0]
    assert updated["city"] == "Delhi"

def test_update_client_invalid_raises(tmp_path):
    """
    Test that invalid updates raise an error.

    Updating a client with invalid data (e.g., empty name)
    should trigger validation and raise a ValueError.
    """
    storage = JsonStorage(tmp_path / "records.json")
    repo = RecordRepository(storage)

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
    repo.create_client(client)

    with pytest.raises(ValueError):
        repo.update_client(1, {"name": ""})

def test_update_client_does_not_mutate_on_failure(tmp_path):
    """
    Test that failed updates do not alter the original record.

    This ensures the repository uses an atomic update strategy,
    preserving the original data if validation fails.
    """
    storage = JsonStorage(tmp_path / "records.json")
    repo = RecordRepository(storage)

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
    repo.create_client(client)

    original = repo.records[0].copy()

    with pytest.raises(ValueError):
        repo.update_client(1, {"name": ""})

    assert repo.records[0] == original

def test_update_airline_valid(tmp_path):
    """
    Test updating an airline record with valid data.

    This verifies that the repository correctly updates an airline's
    information when the new data passes validation.
    """
    storage = JsonStorage(tmp_path / "records.json")
    repo = RecordRepository(storage)

    airline = AirlineRecord("Emirates")
    repo.create_airline(airline)

    repo.update_airline(1, {"company_name": "Qatar Airways"})

    updated = repo.records[0]
    assert updated["company_name"] == "Qatar Airways"

def test_update_airline_invalid_raises(tmp_path):
    """
    Test that updating an airline with invalid data raises an error.

    If the airline company name becomes empty, validation should fail
    and the repository should raise a ValueError.
    """
    storage = JsonStorage(tmp_path / "records.json")
    repo = RecordRepository(storage)

    airline = AirlineRecord("Emirates")
    repo.create_airline(airline)

    with pytest.raises(ValueError):
        repo.update_airline(1, {"company_name": ""})

def test_search_client_by_city(tmp_path):
    """
    Test the search functionality for clients by city.

    This verifies that the repository search method correctly filters
    records based on a single search criterion.
    """
    storage = JsonStorage(tmp_path / "records.json")
    repo = RecordRepository(storage)

    client1 = ClientRecord(
        name="John",
        address_line_1="A",
        address_line_2="B",
        address_line_3="C",
        city="Lucknow",
        state="UP",
        zip_code="226001",
        country="India",
        phone_number="123"
    )
    repo.create_client(client1)

    client2 = ClientRecord(
        name="Jane",
        address_line_1="A",
        address_line_2="B",
        address_line_3="C",
        city="Delhi",
        state="DL",
        zip_code="110001",
        country="India",
        phone_number="456"
    )
    repo.create_client(client2)

    results = repo.search("client", {"city": "Lucknow"})

    assert len(results) == 1
    assert results[0]["name"] == "John"

def test_search_multiple_criteria(tmp_path):
    """
    Test searching with multiple criteria.

    This ensures that the search method correctly returns records
    that satisfy all provided conditions.
    """
    storage = JsonStorage(tmp_path / "records.json")
    repo = RecordRepository(storage)

    client = ClientRecord(
        name="John",
        address_line_1="A",
        address_line_2="B",
        address_line_3="C",
        city="Lucknow",
        state="UP",
        zip_code="226001",
        country="India",
        phone_number="123"
    )
    repo.create_client(client)

    results = repo.search("client", {"city": "Lucknow", "state": "UP"})

    assert len(results) == 1

def test_repository_loads_existing_records(tmp_path):
    """
    Test that the repository correctly loads existing records
    from the storage file during initialization.

    This verifies that previously saved data is restored when
    the application starts.
    """
    file_path = tmp_path / "records.json"
    storage = JsonStorage(file_path)

    # Pre-populate file
    existing = [
        {"type": "client", "id": 5, "name": "John",
         "address_line_1": "A", "address_line_2": "B",
         "address_line_3": "C", "city": "Lucknow",
         "state": "UP", "zip_code": "226001",
         "country": "India", "phone_number": "123"}
    ]
    storage.save(existing)

    repo = RecordRepository(storage)

    assert len(repo.records) == 1
    assert repo.records[0]["id"] == 5

def test_repository_recalculates_ids_on_load(tmp_path):
    """
    Test that the repository recalculates ID counters when loading data.

    This ensures that new records created after loading existing data
    continue from the correct next ID values.
    """
    file_path = tmp_path / "records.json"
    storage = JsonStorage(file_path)

    existing = [
        {"type": "client", "id": 3, "name": "John",
         "address_line_1": "A", "address_line_2": "B",
         "address_line_3": "C", "city": "Lucknow",
         "state": "UP", "zip_code": "226001",
         "country": "India", "phone_number": "123"},
        {"type": "airline", "id": 7, "company_name": "Emirates"}
    ]
    storage.save(existing)

    repo = RecordRepository(storage)

    assert repo.next_client_id == 4
    assert repo.next_airline_id == 8

def test_repository_persistence_cycle(tmp_path):
    """
    Test the full persistence cycle of the repository.

    This verifies that:
    1. Records can be created in the repository
    2. The repository can save records to storage
    3. A new repository instance can reload those records
    4. ID counters remain correct after loading
    """
    file_path = tmp_path / "records.json"
    storage = JsonStorage(file_path)

    repo = RecordRepository(storage)

    client = ClientRecord(
        name="John",
        address_line_1="A",
        address_line_2="B",
        address_line_3="C",
        city="Lucknow",
        state="UP",
        zip_code="226001",
        country="India",
        phone_number="123"
    )
    repo.create_client(client)

    repo.save()

    # Create new repo instance
    repo2 = RecordRepository(storage)

    assert len(repo2.records) == 1
    assert repo2.next_client_id == 2