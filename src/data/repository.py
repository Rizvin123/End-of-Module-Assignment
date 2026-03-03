from typing import List, Dict, Any
from src.data.storage import JsonStorage
from src.record.client import ClientRecord
from src.record.airline import AirlineRecord
from src.record.flight import FlightRecord



class RecordRepository:
    def __init__(self, storage: JsonStorage) -> None:
        self.storage = storage
        self.records: List[Dict[str, Any]] = []
        self.next_client_id: int = 1
        self.next_airline_id: int = 1
        self._load()

    def _load(self) -> None:
        if not self.storage.exists():
            self.records = []
            return
        
        self.records = self.storage.load()
        self._recalculate_ids()

    def _recalculate_ids(self) -> None:
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
        return [r for r in self.records if r["type"] == record_type]
    
    def get_client_by_id(self, client_id: int) -> dict | None:
        for record in self.records:
            if record["type"] == "client" and record["id"] == client_id:
                return record
        return None
    
    def get_airline_by_id(self, airline_id: int) -> dict | None:
        for record in self.records:
            if record["type"] == "airline" and record["id"] == airline_id:
                return record
        return None

    def create_client(self, client: ClientRecord) -> None:
        client.validate()
        client.id = self.next_client_id
        self.next_client_id += 1
        self.records.append(client.to_dict())

    def create_airline(self, airline: AirlineRecord) -> None:
        airline.validate()
        airline.id = self.next_airline_id
        self.next_airline_id += 1
        self.records.append(airline.to_dict())

    def create_flight(self, flight: FlightRecord) -> None:
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
        self.storage.save(self.records)