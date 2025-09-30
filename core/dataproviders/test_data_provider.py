"""
Test Data Provider base class
"""
import logging
from typing import List, Dict, Any
from abc import ABC, abstractmethod


class TestDataProvider(ABC):
    """Abstract base class for test data providers"""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def load_data(self, source: str) -> List[Dict[str, Any]]:
        """Load test data from source"""
        pass

    @abstractmethod
    def get_data_by_test_name(self, test_name: str) -> List[Dict[str, Any]]:
        """Get test data filtered by test name"""
        pass

    def filter_data(self, data: List[Dict[str, Any]],
                    filter_criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Filter data based on criteria"""
        filtered_data = []
        for record in data:
            if all(record.get(key) == value for key, value in filter_criteria.items()):
                filtered_data.append(record)
        return filtered_data
