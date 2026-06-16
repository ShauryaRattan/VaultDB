from .storage import Storage


class Query:
    """
    VaultDB Query Engine
    Provides simple filtering and querying over collections.
    """

    def __init__(self, storage: Storage):
        self.storage = storage

    def where(self, collection: str, **filters) -> list:
        """
        Filter records by field values.
        Example: query.where("users", name="Alice", age=30)
        """
        data = self.storage.find_all(collection)
        results = []
        for record in data:
            if all(record.get(k) == v for k, v in filters.items()):
                results.append(record)
        return results

    def count(self, collection: str, **filters) -> int:
        """Count records matching filters."""
        return len(self.where(collection, **filters))

    def exists(self, collection: str, **filters) -> bool:
        """Check if any record matches the filters."""
        return self.count(collection, **filters) > 0

    def order_by(self, collection: str, field: str, descending: bool = False) -> list:
        """Return all records sorted by a field."""
        data = self.storage.find_all(collection)
        return sorted(data, key=lambda r: r.get(field, 0), reverse=descending)

    def limit(self, collection: str, n: int) -> list:
        """Return first n records."""
        return self.storage.find_all(collection)[:n]
