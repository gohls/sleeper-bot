import os
import json
from datetime import datetime

class LocalStorage:
    def __init__(self, storage_file='local_storage.json'):
        self.storage_file = storage_file
        self.data = self._load_storage()

    def _load_storage(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return {}
        return {}

    def _save_storage(self):
        with open(self.storage_file, 'w') as file:
            json.dump(self.data, file, default=self._json_serial)

    def _json_serial(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError("Type not serializable")

    def save(self, key, value):
        self.data[key] = value
        self._save_storage()

    def load(self, key):
        value = self.data.get(key)
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                pass
        return value

    def delete(self, key):
        if key in self.data:
            del self.data[key]
            self._save_storage()

    def clear(self):
        self.data = {}
        self._save_storage()