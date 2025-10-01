"""
Configuration Reader Utility for loading properties files
"""
import configparser
import os
from typing import Dict, Any
from pathlib import Path


class ConfigReader:
    """Utility class to read configuration from properties files"""

    def __init__(self, config_file: str = None):
        self.config = configparser.ConfigParser()
        self.base_path = Path(__file__).parent.parent.parent.parent.parent

        if config_file is None:
            config_file = self.base_path / "config" / "config.properties"

        self.config_file = config_file
        self._load_config()
        self._load_environment_config()

    def _load_config(self):
        """Load configuration with flexible parsing"""
        if os.path.exists(self.config_file):
            # Try standard INI parsing first
            try:
                self.config.read(self.config_file)
            except:
                # Fallback to properties format
                self._load_properties_file()
        else:
            raise FileNotFoundError(f"Configuration file not found: {self.config_file}")

    def _load_properties_file(self):
        """Load Java-style properties file"""
        with open(self.config_file, 'r') as f:
            # Create a default section
            content = '[DEFAULT]\n' + f.read()
            self.config.read_string(content)

    def _load_environment_config(self):
        """Load environment specific configuration"""
        environment = self.get_property("app.environment", "qa")
        env_config_file = self.base_path / "config" / "environments" / f"{environment}.properties"

        if os.path.exists(env_config_file):
            self.config.read(env_config_file)

    def get_property(self, key: str, default_value: Any = None) -> Any:
        """Get property value from config file"""
        try:
            if '.' in key:
                section, option = key.rsplit('.', 1)
                return self.config.get(section, option)
            else:
                # Search in all sections
                for section in self.config.sections():
                    try:
                        return self.config.get(section, key)
                    except configparser.NoOptionError:
                        continue
                return default_value
        except (configparser.NoSectionError, configparser.NoOptionError):
            return default_value

    def get_int_property(self, key: str, default_value: int = 0) -> int:
        """Get integer property value"""
        value = self.get_property(key, default_value)
        return int(value) if value is not None else default_value

    def get_bool_property(self, key: str, default_value: bool = False) -> bool:
        """Get boolean property value"""
        value = self.get_property(key, default_value)
        if isinstance(value, str):
            return value.lower() in ['true', 'yes', '1', 'on']
        return bool(value) if value is not None else default_value

    def get_list_property(self, key: str, separator: str = ',') -> list:
        """Get list property value"""
        value = self.get_property(key, "")
        return [item.strip() for item in value.split(separator) if item.strip()]

    def get_all_properties(self) -> Dict[str, Any]:
        """Get all properties as dictionary"""
        properties = {}
        for section in self.config.sections():
            properties[section] = dict(self.config.items(section))
        return properties
