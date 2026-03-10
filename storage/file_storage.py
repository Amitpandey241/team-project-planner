import json
import os

class FileStorage:

    @staticmethod
    def read(path):

        if not os.path.exists(path):
            return []

        with open(path, "r") as f:
            return json.load(f)

    @staticmethod
    def write(path, data):

        with open(path, "w") as f:
            json.dump(data, f, indent=2)