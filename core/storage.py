import json
import os


class Storage:
    """
    VaultDB Storage Engine
    Handles reading and writing data to disk using JSON-based flat files.
    Each collection is stored as a separate .json file.
    """

    def __init__(self, data_dir: str = "./data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

    def _get_path(self, collection: str) -> str:
        return os.path.join(self.data_dir, f"{collection}.json")

    def _load(self, collection: str) -> list:
        path = self._get_path(collection)
        if not os.path.exists(path):
            return []
        with open(path, "r") as f:
            return json.load(f)

    def _save(self, collection: str, data: list) -> None:
        with open(self._get_path(collection), "w") as f:
            json.dump(data, f, indent=2)

    def insert(self, collection: str, record: dict) -> dict:
        """Insert a record into a collection."""
        data = self._load(collection)
        # Auto-assign ID
        record["_id"] = len(data) + 1
        data.append(record)
        self._save(collection, data)
        return record

    def find_all(self, collection: str) -> list:
        """Return all records in a collection."""
        return self._load(collection)

    def find_by_id(self, collection: str, id: int) -> dict | None:
        """Find a single record by ID."""
        data = self._load(collection)
        for record in data:
            if record.get("_id") == id:
                return record
        return None

    def update(self, collection: str, id: int, updates: dict) -> dict | None:
        """Update a record by ID."""
        data = self._load(collection)
        for record in data:
            if record.get("_id") == id:
                record.update(updates)
                self._save(collection, data)
                return record
        return None

    def delete(self, collection: str, id: int) -> bool:
        """Delete a record by ID."""
        data = self._load(collection)
        new_data = [r for r in data if r.get("_id") != id]
        if len(new_data) == len(data):
            return False
        self._save(collection, new_data)
        return True
