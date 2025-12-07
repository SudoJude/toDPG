import configparser
import os
from backend import globals

class ConfigManager:
    def __init__(self):
        self.config_file = globals.CONFIG_FILE
        self.config = configparser.ConfigParser()
        self._load_config()

    def _load_config(self):
        if not os.path.exists(self.config_file):
            self._create_default_config()
        else:
            self.config.read(self.config_file)
            # Merge with defaults to ensure all keys exist
            self._ensure_defaults()

    def _create_default_config(self):
        self.config.read_dict(globals.DEFAULT_CONFIG)
        self.save_config()

    def _ensure_defaults(self):
        changed = False
        for section, options in globals.DEFAULT_CONFIG.items():
            if not self.config.has_section(section):
                self.config.add_section(section)
                changed = True
            for key, value in options.items():
                if not self.config.has_option(section, key):
                    self.config.set(section, key, value)
                    changed = True
        if changed:
            self.save_config()

    def save_config(self):
        with open(self.config_file, 'w') as f:
            self.config.write(f)

    def get_config(self):
        config_dict = {}
        for section in self.config.sections():
            config_dict[section] = dict(self.config.items(section))
        return config_dict

    def update_config(self, new_config):
        for section, options in new_config.items():
            if not self.config.has_section(section):
                self.config.add_section(section)
            for key, value in options.items():
                self.config.set(section, key, str(value))
        self.save_config()

    def get(self, section, key, fallback=None):
        return self.config.get(section, key, fallback=fallback)

    def getint(self, section, key, fallback=None):
        return self.config.getint(section, key, fallback=fallback)

    def getboolean(self, section, key, fallback=None):
        return self.config.getboolean(section, key, fallback=fallback)
