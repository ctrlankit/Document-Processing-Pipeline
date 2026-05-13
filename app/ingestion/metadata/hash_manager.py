"""File hash management utilities."""

import hashlib
import json
import os

HASH_FILE = "data/processed/file_hashes.json"
class HashManager:

    @staticmethod
    def Generate_hash(file_path: str) -> str:
        try:

            hasher = hashlib.md5()

            with open(file_path, "rb") as f:
                buf = f.read()

                hasher.update(buf)

            return hasher.hexdigest()
        except Exception as e:
            print(f"Error generating hash for file {file_path}: {e}")
            return ""
        
    @staticmethod
    def save_hash(hashes: dict) -> None:
        try:
            os.makedirs("data/processed", exist_ok=True)

            with open(HASH_FILE, "w") as file:
                json.dump(hashes, file, indent=4)
        except Exception as e:
            print(f"Error saving hashes: {e}")


    @staticmethod
    def load_hashes() -> dict:
        try:
            if os.path.exists(HASH_FILE):
                with open(HASH_FILE, "r") as file:
                    return json.load(file)
            else:
                return {}
        except Exception as e:
            print(f"Error loading hashes: {e}")
            return {}
        
    @staticmethod
    def is_file_changed(file_path: str) -> bool:
        try:
            current_hash = HashManager.Generate_hash(file_path)

            saved_hashes = HashManager.load_hashes()

            filename = os.path.basename(file_path)

            old_hash = saved_hashes.get(filename)

            if old_hash == current_hash:
                return False

            saved_hashes[filename] = current_hash

            HashManager.save_hash(saved_hashes)

            return True
        except Exception as e:
            print(f"Error checking if file {file_path} has changed: {e}")
            return False