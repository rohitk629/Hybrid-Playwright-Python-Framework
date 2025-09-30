"""
Excel Data Provider
"""
from typing import List, Dict, Any
from core.dataproviders.test_data_provider import TestDataProvider
from core.utils.excel_utility import ExcelUtility
import pytest


class ExcelDataProvider(TestDataProvider):
    """Data provider for Excel files"""

    def __init__(self):
        super().__init__()
        self.excel_utility = ExcelUtility()

    def load_data(self, file_path: str, sheet_name: str = None) -> List[Dict[str, Any]]:
        """Load data from Excel file"""
        try:
            data = self.excel_utility.read_excel_data(file_path, sheet_name)
            self.logger.info(f"Loaded {len(data)} records from Excel: {file_path}")
            return data
        except Exception as e:
            self.logger.error(f"Error loading Excel data: {e}")
            raise

    def get_data_by_test_name(self, file_path: str, test_name: str,
                              sheet_name: str = None) -> List[Dict[str, Any]]:
        """Get test data filtered by test name"""
        data = self.load_data(file_path, sheet_name)
        filtered_data = [record for record in data if record.get('TestName') == test_name]
        self.logger.info(f"Found {len(filtered_data)} records for test: {test_name}")
        return filtered_data

    @staticmethod
    def parametrize_from_excel(file_path: str, sheet_name: str = None):
        """Decorator to parametrize tests from Excel"""

        def decorator(func):
            excel_provider = ExcelDataProvider()
            test_data = excel_provider.load_data(file_path, sheet_name)

            # Convert list of dicts to list of tuples for pytest parametrize
            param_names = list(test_data[0].keys()) if test_data else []
            param_values = [tuple(record.values()) for record in test_data]

            return pytest.mark.parametrize(','.join(param_names), param_values)(func)

        return decorator