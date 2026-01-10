import json
import os

class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file

    def load(self):
        config = {}
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    config = json.load(f)
            except Exception:
                pass
        return config

    def update(self, key, value):
        config = self.load()
        config[key] = value
        try:
            with open(self.config_file, "w") as f:
                json.dump(config, f)
        except Exception:
            pass