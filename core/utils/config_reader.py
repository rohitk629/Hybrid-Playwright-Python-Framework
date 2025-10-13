"""
Configuration Reader Utility for loading YAML files
"""
import yaml
import os
from typing import Dict, Any, List
from pathlib import Path


class ConfigReader:
    """Utility class to read configuration from YAML files"""

    def __init__(self, config_file: str = None):
        self.config = {}
        self.base_path = Path(__file__).parent.parent.parent

        if config_file is None:
            config_file = self.base_path / "config" / "config.yaml"

        self.config_file = config_file
        self._load_config()
        self._load_environment_config()

    def _load_config(self):
        """Load main configuration from YAML file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.config = yaml.safe_load(f) or {}
                print(f"Loaded config from: {self.config_file}")
            except Exception as e:
                print(f"Error loading config: {e}")
                self.config = {}
        else:
            print(f"Configuration file not found: {self.config_file}")
            self.config = {}

    def _load_environment_config(self):
        """Load environment specific configuration"""
        try:
            environment = self.get_property("app.environment", "qa")
            env_config_file = self.base_path / "config" / "environments" / f"{environment}.yaml"

            if os.path.exists(env_config_file):
                with open(env_config_file, 'r') as f:
                    env_config = yaml.safe_load(f) or {}
                    # Merge environment config with main config
                    self._deep_merge(self.config, env_config)
                print(f"Loaded environment config from: {env_config_file}")
        except Exception as e:
            print(f"Error loading environment config: {e}")

    def _deep_merge(self, base_dict: dict, update_dict: dict) -> dict:
        """Deep merge update_dict into base_dict"""
        for key, value in update_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                self._deep_merge(base_dict[key], value)
            else:
                base_dict[key] = value
        return base_dict

    def get_property(self, key: str, default_value: Any = None) -> Any:
        """
        Get property value from config using dot notation

        Args:
            key: Property key in dot notation (e.g., 'app.base_url')
            default_value: Default value if key not found

        Returns:
            Property value or default
        """
        try:
            keys = key.split('.')
            value = self.config

            for k in keys:
                if isinstance(value, dict):
                    value = value.get(k)
                    if value is None:
                        return default_value
                else:
                    return default_value

            return value if value is not None else default_value

        except Exception as e:
            print(f"Error getting property '{key}': {e}")
            return default_value

    def get_int_property(self, key: str, default_value: int = 0) -> int:
        """Get integer property value"""
        value = self.get_property(key, default_value)
        try:
            return int(value) if value is not None else default_value
        except (ValueError, TypeError):
            return default_value

    def get_bool_property(self, key: str, default_value: bool = False) -> bool:
        """Get boolean property value"""
        value = self.get_property(key, default_value)
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ['true', 'yes', '1', 'on']
        return default_value

    def get_list_property(self, key: str, default_value: list = None) -> List:
        """Get list property value"""
        value = self.get_property(key, default_value or [])
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            # If it's a string, split by comma
            return [item.strip() for item in value.split(',') if item.strip()]
        return default_value or []

    def get_dict_property(self, key: str, default_value: dict = None) -> Dict:
        """Get dictionary property value"""
        value = self.get_property(key, default_value or {})
        if isinstance(value, dict):
            return value
        return default_value or {}

    def get_all_properties(self) -> Dict[str, Any]:
        """Get all properties as dictionary"""
        return self.config.copy()

    def set_property(self, key: str, value: Any):
        """
        Set property value using dot notation

        Args:
            key: Property key in dot notation
            value: Value to set
        """
        keys = key.split('.')
        current = self.config

        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]

        current[keys[-1]] = value

    def save_config(self, output_file: str = None):
        """
        Save current configuration to YAML file

        Args:
            output_file: Output file path (default: overwrite current config file)
        """
        output_path = output_file or self.config_file
        try:
            with open(output_path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False, sort_keys=False)
            print(f"Configuration saved to: {output_path}")
        except Exception as e:
            print(f"Error saving configuration: {e}")

    def reload_config(self):
        """Reload configuration from files"""
        self._load_config()
        self._load_environment_config()