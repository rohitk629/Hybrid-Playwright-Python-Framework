"""
JSON Data Provider
"""
from typing import List, Dict, Any
from core.dataproviders.test_data_provider import TestDataProvider
from core.utils.json_utility import JSONUtility
import pytest


class JSONDataProvider(TestDataProvider):
    """Data provider for JSON files"""

    def __init__(self):
        super().__init__()
        self.json_utility = JSONUtility()

    def load_data(self, file_path: str, json_path: str = None) -> List[Dict[str, Any]]:
        """Load data from JSON file"""
        try:
            data = self.json_utility.read_json_file(file_path)

            # Extract data using JSON path if provided
            if json_path:
                data = self.json_utility.extract_value_by_json_path(data, json_path)

            # Ensure data is a list
            if not isinstance(data, list):
                data = [data]

            self.logger.info(f"Loaded {len(data)} records from JSON: {file_path}")
            return data
        except Exception as e:
            self.logger.error(f"Error loading JSON data: {e}")
            raise

    def get_data_by_test_name(self, file_path: str, test_name: str) -> List[Dict[str, Any]]:
        """Get test data filtered by test name"""
        data = self.load_data(file_path)
        filtered_data = [record for record in data if record.get('test_name') == test_name]
        self.logger.info(f"Found {len(filtered_data)} records for test: {test_name}")
        return filtered_data

    @staticmethod
    def parametrize_from_json(file_path: str, json_path: str = None):
        """Decorator to parametrize tests from JSON"""

        def decorator(func):
            json_provider = JSONDataProvider()
            test_data = json_provider.load_data(file_path, json_path)

            # Convert list of dicts to list of tuples for pytest parametrize
            param_names = list(test_data[0].keys()) if test_data else []
            param_values = [tuple(record.values()) for record in test_data]

            return pytest.mark.parametrize(','.join(param_names), param_values)(func)

        return decorator