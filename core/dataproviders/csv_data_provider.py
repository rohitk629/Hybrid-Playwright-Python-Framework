"""
CSV Data Provider Module
Provides functionality to read and process CSV files for test data management
"""

import csv
import os
from typing import List, Dict, Any, Optional, Iterator
from pathlib import Path
import logging
from core.utils.file_utility import FileUtility
from core.constants.error_messages import ErrorMessages

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CSVDataProvider:
    """
    Provides methods to read and process CSV files for test data
    Supports various data retrieval patterns and filtering options
    """

    def __init__(self, base_path: str = None):
        """
        Initialize CSV Data Provider

        Args:
            base_path: Base path for CSV files. Defaults to test_data/csv/
        """
        if base_path is None:
            self.base_path = Path(__file__).parent.parent.parent.parent.parent.parent / "test_data" / "csv"
        else:
            self.base_path = Path(base_path)

        self.file_utility = FileUtility()
        logger.info(f"CSVDataProvider initialized with base path: {self.base_path}")

    def read_csv(self, file_name: str, encoding: str = 'utf-8') -> List[Dict[str, Any]]:
        """
        Read CSV file and return list of dictionaries

        Args:
            file_name: Name of the CSV file
            encoding: File encoding (default: utf-8)

        Returns:
            List of dictionaries containing CSV data

        Raises:
            FileNotFoundError: If CSV file doesn't exist
            Exception: For other CSV reading errors
        """
        file_path = self.base_path / file_name

        try:
            if not file_path.exists():
                raise FileNotFoundError(f"CSV file not found: {file_path}")

            logger.info(f"Reading CSV file: {file_path}")

            data = []
            with open(file_path, 'r', encoding=encoding, newline='') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    # Convert string values to appropriate types
                    processed_row = self._process_row(row)
                    data.append(processed_row)

            logger.info(f"Successfully read {len(data)} rows from {file_name}")
            return data

        except FileNotFoundError as e:
            logger.error(f"File not found error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error reading CSV file {file_name}: {str(e)}")
            raise Exception(f"Failed to read CSV file: {str(e)}")

    def read_csv_as_list(self, file_name: str, encoding: str = 'utf-8') -> List[List[str]]:
        """
        Read CSV file and return list of lists (including headers)

        Args:
            file_name: Name of the CSV file
            encoding: File encoding

        Returns:
            List of lists containing CSV data
        """
        file_path = self.base_path / file_name

        try:
            if not file_path.exists():
                raise FileNotFoundError(f"CSV file not found: {file_path}")

            logger.info(f"Reading CSV file as list: {file_path}")

            data = []
            with open(file_path, 'r', encoding=encoding, newline='') as csv_file:
                csv_reader = csv.reader(csv_file)
                data = list(csv_reader)

            logger.info(f"Successfully read {len(data)} rows from {file_name}")
            return data

        except Exception as e:
            logger.error(f"Error reading CSV file {file_name}: {str(e)}")
            raise

    def get_test_data(self, file_name: str, test_case_id: str = None) -> List[Dict[str, Any]]:
        """
        Get test data from CSV file, optionally filtered by test case ID

        Args:
            file_name: Name of the CSV file
            test_case_id: Optional test case ID to filter data

        Returns:
            List of test data dictionaries
        """
        data = self.read_csv(file_name)

        if test_case_id:
            filtered_data = [row for row in data if row.get('test_case_id') == test_case_id]
            logger.info(f"Filtered {len(filtered_data)} rows for test case: {test_case_id}")
            return filtered_data

        return data

    def get_row_by_column_value(self, file_name: str, column_name: str,
                                column_value: Any) -> Optional[Dict[str, Any]]:
        """
        Get first row matching column value

        Args:
            file_name: Name of the CSV file
            column_name: Column name to search
            column_value: Value to match

        Returns:
            Dictionary containing matched row or None
        """
        data = self.read_csv(file_name)

        for row in data:
            if str(row.get(column_name)) == str(column_value):
                logger.info(f"Found matching row for {column_name}={column_value}")
                return row

        logger.warning(f"No matching row found for {column_name}={column_value}")
        return None

    def get_all_rows_by_column_value(self, file_name: str, column_name: str,
                                     column_value: Any) -> List[Dict[str, Any]]:
        """
        Get all rows matching column value

        Args:
            file_name: Name of the CSV file
            column_name: Column name to search
            column_value: Value to match

        Returns:
            List of dictionaries containing matched rows
        """
        data = self.read_csv(file_name)

        filtered_data = [row for row in data if str(row.get(column_name)) == str(column_value)]
        logger.info(f"Found {len(filtered_data)} matching rows for {column_name}={column_value}")

        return filtered_data

    def get_column_data(self, file_name: str, column_name: str) -> List[Any]:
        """
        Get all values from a specific column

        Args:
            file_name: Name of the CSV file
            column_name: Column name to extract

        Returns:
            List of column values
        """
        data = self.read_csv(file_name)

        column_data = [row.get(column_name) for row in data if column_name in row]
        logger.info(f"Extracted {len(column_data)} values from column: {column_name}")

        return column_data

    def get_unique_column_values(self, file_name: str, column_name: str) -> List[Any]:
        """
        Get unique values from a specific column

        Args:
            file_name: Name of the CSV file
            column_name: Column name

        Returns:
            List of unique column values
        """
        column_data = self.get_column_data(file_name, column_name)
        unique_values = list(set(column_data))

        logger.info(f"Found {len(unique_values)} unique values in column: {column_name}")
        return unique_values

    def filter_data(self, file_name: str, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Filter CSV data based on multiple criteria

        Args:
            file_name: Name of the CSV file
            filters: Dictionary of column_name: value pairs to filter

        Returns:
            List of filtered dictionaries
        """
        data = self.read_csv(file_name)

        filtered_data = data
        for column, value in filters.items():
            filtered_data = [row for row in filtered_data if str(row.get(column)) == str(value)]

        logger.info(f"Filtered data: {len(filtered_data)} rows match criteria")
        return filtered_data

    def get_row_by_index(self, file_name: str, index: int) -> Optional[Dict[str, Any]]:
        """
        Get row by index (0-based)

        Args:
            file_name: Name of the CSV file
            index: Row index

        Returns:
            Dictionary containing row data or None
        """
        data = self.read_csv(file_name)

        if 0 <= index < len(data):
            return data[index]
        else:
            logger.warning(f"Index {index} out of range for {file_name}")
            return None

    def get_headers(self, file_name: str) -> List[str]:
        """
        Get column headers from CSV file

        Args:
            file_name: Name of the CSV file

        Returns:
            List of column headers
        """
        file_path = self.base_path / file_name

        try:
            with open(file_path, 'r', encoding='utf-8', newline='') as csv_file:
                csv_reader = csv.reader(csv_file)
                headers = next(csv_reader)

            logger.info(f"Retrieved headers from {file_name}: {headers}")
            return headers

        except Exception as e:
            logger.error(f"Error reading headers from {file_name}: {str(e)}")
            raise

    def get_row_count(self, file_name: str) -> int:
        """
        Get total number of data rows (excluding header)

        Args:
            file_name: Name of the CSV file

        Returns:
            Number of data rows
        """
        data = self.read_csv(file_name)
        row_count = len(data)

        logger.info(f"Row count for {file_name}: {row_count}")
        return row_count

    def write_csv(self, file_name: str, data: List[Dict[str, Any]],
                  encoding: str = 'utf-8', mode: str = 'w') -> bool:
        """
        Write data to CSV file

        Args:
            file_name: Name of the CSV file
            data: List of dictionaries to write
            encoding: File encoding
            mode: Write mode ('w' for overwrite, 'a' for append)

        Returns:
            True if successful, False otherwise
        """
        file_path = self.base_path / file_name

        try:
            # Ensure directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)

            if not data:
                logger.warning("No data to write")
                return False

            # Get headers from first dictionary
            headers = list(data[0].keys())

            with open(file_path, mode, encoding=encoding, newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=headers)

                if mode == 'w':
                    writer.writeheader()

                writer.writerows(data)

            logger.info(f"Successfully wrote {len(data)} rows to {file_name}")
            return True

        except Exception as e:
            logger.error(f"Error writing to CSV file {file_name}: {str(e)}")
            return False

    def append_row(self, file_name: str, row_data: Dict[str, Any]) -> bool:
        """
        Append a single row to CSV file

        Args:
            file_name: Name of the CSV file
            row_data: Dictionary containing row data

        Returns:
            True if successful, False otherwise
        """
        return self.write_csv(file_name, [row_data], mode='a')

    def update_row(self, file_name: str, column_name: str,
                   column_value: Any, updated_data: Dict[str, Any]) -> bool:
        """
        Update row(s) matching column value

        Args:
            file_name: Name of the CSV file
            column_name: Column to match
            column_value: Value to match
            updated_data: Dictionary containing updated values

        Returns:
            True if successful, False otherwise
        """
        try:
            data = self.read_csv(file_name)
            updated = False

            for row in data:
                if str(row.get(column_name)) == str(column_value):
                    row.update(updated_data)
                    updated = True

            if updated:
                self.write_csv(file_name, data, mode='w')
                logger.info(f"Updated rows in {file_name} where {column_name}={column_value}")
                return True
            else:
                logger.warning(f"No rows found to update in {file_name}")
                return False

        except Exception as e:
            logger.error(f"Error updating CSV file {file_name}: {str(e)}")
            return False

    def delete_row(self, file_name: str, column_name: str, column_value: Any) -> bool:
        """
        Delete row(s) matching column value

        Args:
            file_name: Name of the CSV file
            column_name: Column to match
            column_value: Value to match

        Returns:
            True if successful, False otherwise
        """
        try:
            data = self.read_csv(file_name)
            original_count = len(data)

            filtered_data = [row for row in data
                             if str(row.get(column_name)) != str(column_value)]

            deleted_count = original_count - len(filtered_data)

            if deleted_count > 0:
                self.write_csv(file_name, filtered_data, mode='w')
                logger.info(f"Deleted {deleted_count} rows from {file_name}")
                return True
            else:
                logger.warning(f"No rows found to delete in {file_name}")
                return False

        except Exception as e:
            logger.error(f"Error deleting from CSV file {file_name}: {str(e)}")
            return False

    def csv_to_pytest_params(self, file_name: str, test_case_id: str = None) -> List[tuple]:
        """
        Convert CSV data to pytest parametrize format

        Args:
            file_name: Name of the CSV file
            test_case_id: Optional test case ID filter

        Returns:
            List of tuples for pytest parametrization
        """
        data = self.get_test_data(file_name, test_case_id)

        if not data:
            return []

        # Convert list of dicts to list of tuples
        params = [tuple(row.values()) for row in data]
        logger.info(f"Converted {len(params)} rows to pytest parameters")

        return params

    def csv_iterator(self, file_name: str, encoding: str = 'utf-8') -> Iterator[Dict[str, Any]]:
        """
        Create an iterator for large CSV files (memory efficient)

        Args:
            file_name: Name of the CSV file
            encoding: File encoding

        Yields:
            Dictionary for each row
        """
        file_path = self.base_path / file_name

        try:
            with open(file_path, 'r', encoding=encoding, newline='') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    yield self._process_row(row)

        except Exception as e:
            logger.error(f"Error iterating CSV file {file_name}: {str(e)}")
            raise

    def merge_csv_files(self, file_names: List[str], output_file: str) -> bool:
        """
        Merge multiple CSV files into one

        Args:
            file_names: List of CSV file names to merge
            output_file: Output file name

        Returns:
            True if successful, False otherwise
        """
        try:
            all_data = []

            for file_name in file_names:
                data = self.read_csv(file_name)
                all_data.extend(data)

            if all_data:
                self.write_csv(output_file, all_data, mode='w')
                logger.info(f"Merged {len(file_names)} files into {output_file}")
                return True
            else:
                logger.warning("No data to merge")
                return False

        except Exception as e:
            logger.error(f"Error merging CSV files: {str(e)}")
            return False

    def _process_row(self, row: Dict[str, str]) -> Dict[str, Any]:
        """
        Process row to convert string values to appropriate types

        Args:
            row: Dictionary containing row data

        Returns:
            Processed dictionary with typed values
        """
        processed_row = {}

        for key, value in row.items():
            # Try to convert to appropriate type
            if value is None or value == '':
                processed_row[key] = None
            elif value.lower() == 'true':
                processed_row[key] = True
            elif value.lower() == 'false':
                processed_row[key] = False
            elif value.lower() == 'none' or value.lower() == 'null':
                processed_row[key] = None
            else:
                # Try numeric conversion
                try:
                    if '.' in value:
                        processed_row[key] = float(value)
                    else:
                        processed_row[key] = int(value)
                except ValueError:
                    # Keep as string if conversion fails
                    processed_row[key] = value

        return processed_row

    def validate_csv_structure(self, file_name: str, expected_headers: List[str]) -> bool:
        """
        Validate CSV file has expected headers

        Args:
            file_name: Name of the CSV file
            expected_headers: List of expected header names

        Returns:
            True if structure is valid, False otherwise
        """
        try:
            headers = self.get_headers(file_name)

            if set(headers) == set(expected_headers):
                logger.info(f"CSV structure validation passed for {file_name}")
                return True
            else:
                missing = set(expected_headers) - set(headers)
                extra = set(headers) - set(expected_headers)

                if missing:
                    logger.error(f"Missing headers in {file_name}: {missing}")
                if extra:
                    logger.error(f"Extra headers in {file_name}: {extra}")

                return False

        except Exception as e:
            logger.error(f"Error validating CSV structure: {str(e)}")
            return False


# Example usage and utility functions
if __name__ == "__main__":
    # Initialize provider
    csv_provider = CSVDataProvider()

    # Example: Read CSV data
    try:
        data = csv_provider.read_csv("test_data.csv")
        print(f"Total rows: {len(data)}")
        print(f"Sample row: {data[0] if data else 'No data'}")
    except Exception as e:
        print(f"Error: {str(e)}")