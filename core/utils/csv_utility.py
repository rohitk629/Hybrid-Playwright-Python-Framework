"""
CSV Utility for reading and writing CSV files
"""
import csv
import pandas as pd
from typing import List, Dict, Any, Optional
import logging
from pathlib import Path


class CSVUtility:
    """Utility class for CSV operations"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def read_csv_data(self, file_path: str, delimiter: str = ',',
                      encoding: str = 'utf-8') -> List[Dict[str, Any]]:
        """Read data from CSV file and return as list of dictionaries"""
        try:
            data = []
            with open(file_path, 'r', encoding=encoding) as file:
                reader = csv.DictReader(file, delimiter=delimiter)
                for row in reader:
                    # Convert empty strings to None
                    processed_row = {k: v if v != '' else None for k, v in row.items()}
                    data.append(processed_row)

            self.logger.info(f"Successfully read {len(data)} rows from {file_path}")
            return data

        except Exception as e:
            self.logger.error(f"Error reading CSV file {file_path}: {e}")
            raise

    def write_csv_data(self, file_path: str, data: List[Dict[str, Any]],
                       delimiter: str = ',', encoding: str = 'utf-8'):
        """Write data to CSV file"""
        try:
            if not data:
                self.logger.warning("No data to write to CSV file")
                return

            # Create directory if it doesn't exist
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)

            fieldnames = data[0].keys()

            with open(file_path, 'w', newline='', encoding=encoding) as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=delimiter)
                writer.writeheader()
                writer.writerows(data)

            self.logger.info(f"Successfully wrote {len(data)} rows to {file_path}")

        except Exception as e:
            self.logger.error(f"Error writing CSV file {file_path}: {e}")
            raise

    def read_csv_with_pandas(self, file_path: str, **kwargs) -> pd.DataFrame:
        """Read CSV file using pandas for advanced operations"""
        try:
            df = pd.read_csv(file_path, **kwargs)
            self.logger.info(f"Successfully read CSV with pandas: {len(df)} rows")
            return df

        except Exception as e:
            self.logger.error(f"Error reading CSV with pandas {file_path}: {e}")
            raise

    def filter_csv_data(self, file_path: str, filter_conditions: Dict[str, Any],
                        delimiter: str = ',') -> List[Dict[str, Any]]:
        """Filter CSV data based on conditions"""
        try:
            df = pd.read_csv(file_path, delimiter=delimiter)

            # Apply filters
            for column, value in filter_conditions.items():
                df = df[df[column] == value]

            filtered_data = df.to_dict('records')

            self.logger.info(f"Filtered CSV data: {len(filtered_data)} rows match criteria")
            return filtered_data

        except Exception as e:
            self.logger.error(f"Error filtering CSV data from {file_path}: {e}")
            raise

    def get_column_values(self, file_path: str, column_name: str,
                          delimiter: str = ',') -> List[Any]:
        """Get all values from specific column"""
        try:
            df = pd.read_csv(file_path, delimiter=delimiter)
            column_values = df[column_name].tolist()

            self.logger.info(f"Retrieved {len(column_values)} values from column {column_name}")
            return column_values

        except Exception as e:
            self.logger.error(f"Error getting column values from {file_path}: {e}")
            raise

    def append_row_to_csv(self, file_path: str, row_data: Dict[str, Any],
                          delimiter: str = ','):
        """Append single row to existing CSV file"""
        try:
            with open(file_path, 'a', newline='', encoding='utf-8') as file:
                if file.tell() == 0:  # File is empty, write header
                    writer = csv.DictWriter(file, fieldnames=row_data.keys(), delimiter=delimiter)
                    writer.writeheader()
                else:
                    writer = csv.DictWriter(file, fieldnames=row_data.keys(), delimiter=delimiter)

                writer.writerow(row_data)

            self.logger.info(f"Successfully appended row to {file_path}")

        except Exception as e:
            self.logger.error(f"Error appending row to CSV file {file_path}: {e}")
            raise