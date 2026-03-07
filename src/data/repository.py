from typing import List, Dict, Any
from src.data.storage import JsonStorage
from src.record.client import ClientRecord
from src.record.airline import AirlineRecord
from src.record.flight import FlightRecord



class RecordRepository:
    """
    Central data management layer of the application.

    Responsibilities:
    - Maintain in memory list of all records (clients, airlines, flights).
    - Enforce business rules (IDs, relationships, integrity)
    - Provide CRUD operations for the GUI
    - Coordinate persistence with the storage layer
    """
    def __init__(self, storage: JsonStorage) -> None:
        """
        Initialize repository with a storage backend.

        The repository loads existing data from disk and
        reconstructs ID counters so new records continue
        from the correct values.
        """
        self.storage = storage
        self.records: List[Dict[str, Any]] = []
        self.next_client_id: int = 1
        self.next_airline_id: int = 1
        self._load()

    def _load(self) -> None:
        """
        Load records from the storage layer.

        If no data file exists, the repository starts empty.
        Otherwise records are loaded and ID counters are recalculated.
        """
        if not self.storage.exists():
            self.records = []
            return
        
        self.records = self.storage.load()
        self._recalculate_ids()

    def _recalculate_ids(self) -> None:
        """
        Recalculate the next available IDs for clients and airlines.

        This ensures ID continuity when the application restarts.
        Example:
        If the highest client ID stored is 5, the next ID becomes 6.
        """
        max_client = 0
        max_airline = 0

        for record in self.records:
            if record["type"] == "client":
                max_client = max(max_client, record["id"])
            elif record["type"] == "airline":
                max_airline = max(max_airline, record["id"])

        self.next_client_id = max_client + 1
        self.next_airline_id = max_airline + 1

    def get_all_by_type(self, record_type: str) -> list:
        """
        Return all records of a specific type.

        Used by the GUI to populate tables for:
        - Clients
        - Airlines
        - Flights
        """
        return [r for r in self.records if r["type"] == record_type]
    
    def get_client_by_id(self, client_id: int) -> dict | None:
        """
        Retrieve a client record by its ID.

        Returns the client dictionary if found,
        otherwise returns None.
        """
        for record in self.records:
            if record["type"] == "client" and record["id"] == client_id:
                return record
        return None
    
    def get_airline_by_id(self, airline_id: int) -> dict | None:
        """
        Retrieve an airline record by its ID.

        Used mainly when displaying flights so the GUI
        can show airline names instead of just IDs.
        """
        for record in self.records:
            if record["type"] == "airline" and record["id"] == airline_id:
                return record
        return None

    def create_client(self, client: ClientRecord) -> None:
        """
        Create a new client record.

        Steps:
        1. Validate the client object
        2. Assign a unique ID
        3. Convert the object to a dictionary
        4. Store it in the repository
        """
        client.validate()
        client.id = self.next_client_id
        self.next_client_id += 1
        self.records.append(client.to_dict())

    def create_airline(self, airline: AirlineRecord) -> None:
        """
        Create a new airline record.

        Similar to client creation:
        - Validate
        - Assign unique ID
        - Store as dictionary
        """
        airline.validate()
        airline.id = self.next_airline_id
        self.next_airline_id += 1
        self.records.append(airline.to_dict())

    def create_flight(self, flight: FlightRecord) -> None:
        """
        Create a new flight record.

        Before creating a flight, the repository enforces
        relational integrity by checking:

        - The referenced client exists
        - The referenced airline exists
        """
        flight.validate()

        client_exists = any(
            r["type"] == "client" and r["id"] == flight.client_id
            for r in self.records
        )

        if not client_exists:
            raise ValueError("Client does not exist.")

        airline_exists = any(
            r["type"] == "airline" and r["id"] == flight.airline_id
            for r in self.records
        )

        if not airline_exists:
            raise ValueError("Airline does not exist.")

        self.records.append(flight.to_dict())

    def delete_client(self, client_id: int) -> None:
        """
        Delete a client record.

        Integrity rule:
        A client cannot be deleted if flights reference it.
        This prevents orphaned flight records.
        """
        client_exists = any(
            r["type"] == "client" and r["id"] == client_id
            for r in self.records
        )

        if not client_exists:
            raise ValueError("Client does not exist.")

        has_flights = any(
            r["type"] == "flight" and r["client_id"] == client_id
            for r in self.records
        )

        if has_flights:
            raise ValueError("Cannot delete client with existing flights.")

        self.records = [
            r for r in self.records
            if not (r["type"] == "client" and r["id"] == client_id)
        ]

    def delete_airline(self, airline_id: int) -> None:
        """
        Delete an airline record.

        Integrity rule:
        An airline cannot be deleted if flights reference it.
        """
        airline_exists = any(
            r["type"] == "airline" and r["id"] == airline_id
            for r in self.records
        )

        if not airline_exists:
            raise ValueError("Airline does not exist.")

        has_flights = any(
            r["type"] == "flight" and r["airline_id"] == airline_id
            for r in self.records
        )

        if has_flights:
            raise ValueError("Cannot delete airline with existing flights.")

        self.records = [
            r for r in self.records
            if not (r["type"] == "airline" and r["id"] == airline_id)
        ]

    def update_client(self, client_id: int, updated_data: dict) -> None:
        """
        Update an existing client record.

        Process:
        1. Locate the client
        2. Create a merged copy of existing + updated data
        3. Validate the merged result
        4. Commit update only if validation succeeds

        This ensures updates are atomic and safe.
        """
        for index, record in enumerate(self.records):
            if record["type"] == "client" and record["id"] == client_id:
                # Create merged copy
                merged = record.copy()
                merged.update(updated_data)

                # Validate using model
                client_obj = ClientRecord.from_dict(merged)
                client_obj.validate()

                # Only commit if validation passes
                self.records[index] = merged
                return

        raise ValueError("Client does not exist.")
    
    def update_airline(self, airline_id: int, updated_data: dict) -> None:
        """
        Update an airline record using the same atomic update strategy
        used for clients.
        """
        for index, record in enumerate(self.records):
            if record["type"] == "airline" and record["id"] == airline_id:
                merged = record.copy()
                merged.update(updated_data)

                airline_obj = AirlineRecord.from_dict(merged)
                airline_obj.validate()

                self.records[index] = merged
                return

        raise ValueError("Airline does not exist.")
    
    def search(self, record_type: str, criteria: dict) -> list:
        """
        Generic search method.

        Filters records by:
        - record type (client, airline, flight)
        - key/value criteria

        Example:
        search("client", {"city": "Lucknow"})
        """
        results = []

        for record in self.records:
            if record["type"] != record_type:
                continue

            match = True
            for key, value in criteria.items():
                if record.get(key) != value:
                    match = False
                    break

            if match:
                results.append(record)

        return results
    
    def save(self) -> None:
        """
        Persist all records to the storage layer.

        Called when the application closes to ensure
        all in-memory changes are written to disk.
        """
        self.storage.save(self.records)