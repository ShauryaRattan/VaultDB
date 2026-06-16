import copy
from .storage import Storage


class Transaction:
    """
    VaultDB Transaction Manager
    Provides basic ACID-like transaction support with rollback capability.
    """

    def __init__(self, storage: Storage):
        self.storage = storage
        self._active = False
        self._snapshots = {}

    def begin(self) -> None:
        """Begin a transaction — snapshot current state."""
        if self._active:
            raise Exception("Transaction already in progress")
        self._active = True
        self._snapshots = {}
        print("[Transaction] Started")

    def _snapshot(self, collection: str) -> None:
        """Take a snapshot of a collection before modifying it."""
        if collection not in self._snapshots:
            self._snapshots[collection] = copy.deepcopy(
                self.storage.find_all(collection)
            )

    def insert(self, collection: str, record: dict) -> dict:
        self._ensure_active()
        self._snapshot(collection)
        return self.storage.insert(collection, record)

    def update(self, collection: str, id: int, updates: dict) -> dict | None:
        self._ensure_active()
        self._snapshot(collection)
        return self.storage.update(collection, id, updates)

    def delete(self, collection: str, id: int) -> bool:
        self._ensure_active()
        self._snapshot(collection)
        return self.storage.delete(collection, id)

    def commit(self) -> None:
        """Commit the transaction — changes are already saved."""
        self._ensure_active()
        self._active = False
        self._snapshots = {}
        print("[Transaction] Committed")

    def rollback(self) -> None:
        """Rollback all changes made during this transaction."""
        self._ensure_active()
        for collection, snapshot in self._snapshots.items():
            self.storage._save(collection, snapshot)
        self._active = False
        self._snapshots = {}
        print("[Transaction] Rolled back")

    def _ensure_active(self) -> None:
        if not self._active:
            raise Exception("No active transaction. Call begin() first.")
