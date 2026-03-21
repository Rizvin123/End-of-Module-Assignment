from src.data.storage import JsonStorage

def test_storage_exists_false(tmp_path):
    """
    Test that the storage correctly reports when the data file does not exist.

    The tmp_path fixture provides a temporary directory for testing.
    Since the file has not been created yet, exists() should return False.
    """
    storage = JsonStorage(tmp_path / "records.json")
    assert not storage.exists()


def test_storage_save_and_load(tmp_path):
    """
    Test that records can be saved to disk and loaded back correctly.

    Steps tested:
    1. Create a JsonStorage instance pointing to a temporary file.
    2. Save a list of record dictionaries to the file.
    3. Confirm that the file now exists.
    4. Load the records from the file and verify they match the original data.

    This ensures that the storage layer correctly handles persistence.
    """
    file_path = tmp_path / "records.json"
    storage = JsonStorage(file_path)

    records = [
        {"type": "client", "id": 1, "name": "John"}
    ]

    storage.save(records)

    assert storage.exists()

    loaded = storage.load()
    assert loaded == records


def test_load_nonexistent_file_returns_empty_list(tmp_path):
    """
    Test that loading from a non-existent file returns an empty list.

    This prevents errors when the application starts for the first time
    and no records.json file has been created yet.
    """
    storage = JsonStorage(tmp_path / "missing.json")
    loaded = storage.load()
    assert loaded == []

def test_storage_overwrites_existing_data(tmp_path):
    """
    Test that saving new records overwrites the existing file contents.

    This ensures that the storage layer correctly updates the data file
    rather than appending or corrupting previous data.
    """
    file_path = tmp_path / "records.json"
    storage = JsonStorage(file_path)

    first_records = [
        {"type": "client", "id": 1, "name": "John"}
    ]

    second_records = [
        {"type": "client", "id": 2, "name": "Alice"}
    ]

    storage.save(first_records)
    storage.save(second_records)

    loaded = storage.load()

    assert loaded == second_records

def test_storage_handles_multiple_records(tmp_path):
    """
    Test that the storage layer correctly saves and loads multiple records.

    This ensures that lists of records maintain their structure and order
    when written to and read from the JSON file.
    """
    file_path = tmp_path / "records.json"
    storage = JsonStorage(file_path)

    records = [
        {"type": "client", "id": 1, "name": "John"},
        {"type": "airline", "id": 1, "company_name": "Emirates"},
        {"type": "flight", "client_id": 1, "airline_id": 1, "start_city": "Delhi", "end_city": "Dubai"}
    ]

    storage.save(records)
    loaded = storage.load()

    assert len(loaded) == 3
    assert loaded == records