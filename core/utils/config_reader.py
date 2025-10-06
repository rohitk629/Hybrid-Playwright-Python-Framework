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
        self.base_path = Path(__file__).parent.parent.parent

        if config_file is None:
            config_file = self.base_path / "config" / "config.properties"

        self.config_file = config_file
        self._load_config()
        self._load_environment_config()

    def _load_config(self):
        """Load configuration with flexible parsing"""
        if os.path.exists(self.config_file):
            try:
                # Read file and add DEFAULT section if missing
                with open(self.config_file, 'r') as f:
                    content = f.read()
                
                # Check if file already has sections
                if not content.strip().startswith('['):
                    content = '[DEFAULT]\n' + content
                
                self.config.read_string(content)
            except Exception as e:
                print(f"Error loading config: {e}")
                # Create minimal default config
                self.config['DEFAULT'] = {}
        else:
            print(f"Configuration file not found: {self.config_file}")
            self.config['DEFAULT'] = {}

    def _load_environment_config(self):
        """Load environment specific configuration"""
        try:
            environment = self.get_property("environment", "qa")
            env_config_file = self.base_path / "config" / "environments" / f"{environment}.properties"

            if os.path.exists(env_config_file):
                self.config.read(env_config_file)
        except Exception as e:
            print(f"Error loading environment config: {e}")

    def get_property(self, key: str, default_value: Any = None) -> Any:
        """Get property value from config file"""
        try:
            # Handle dot notation (section.key)
            if '.' in key:
                parts = key.split('.')
                section = parts[0]
                option = '.'.join(parts[1:])
                
                if section in self.config:
                    return self.config.get(section, option, fallback=default_value)
            
            # Search in all sections
            for section in self.config.sections():
                try:
                    return self.config.get(section, key, fallback=None)
                except:
                    continue
            
            # Try DEFAULT section
            return self.config.get('DEFAULT', key, fallback=default_value)
            
        except Exception as e:
            return default_value

    def get_int_property(self, key: str, default_value: int = 0) -> int:
        """Get integer property value"""
        value = self.get_property(key, default_value)
        try:
            return int(value) if value is not None else default_value
        except:
            return default_value

    def get_bool_property(self, key: str, default_value: bool = False) -> bool:
        """Get boolean property value"""
        value = self.get_property(key, default_value)
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ['true', 'yes', '1', 'on']
        return default_value

    def get_list_property(self, key: str, separator: str = ',') -> list:
        """Get list property value"""
        value = self.get_property(key, "")
        if not value:
            return []
        return [item.strip() for item in str(value).split(separator) if item.strip()]

    def get_all_properties(self) -> Dict[str, Any]:
        """Get all properties as dictionary"""
        properties = {}
        for section in self.config.sections():
            properties[section] = dict(self.config.items(section))
        return properties
