"""
JSON Utility Module
Provides comprehensive JSON file operations and manipulation utilities
Supports reading, writing, validating, comparing, and transforming JSON data
"""

import copy
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Tuple

import jsondiff
import jsonpatch
from jsonpath_ng.ext import parser
from jsonschema import validate, ValidationError, Draft7Validator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JSONUtility:
    """
    Utility class for JSON operations
    Provides methods for reading, writing, validating, and manipulating JSON data
    """

    def __init__(self, base_path: str = None):
        """
        Initialize JSON Utility

        Args:
            base_path: Base path for JSON files. Defaults to test_data/json/
        """
        if base_path is None:
            self.base_path = Path(__file__).parent.parent.parent.parent.parent.parent / "test_data" / "json"
        else:
            self.base_path = Path(base_path)

        self.base_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"JSONUtility initialized with base path: {self.base_path}")

    # ==================== File Operations ====================

    def read_json(self, file_name: str, encoding: str = 'utf-8') -> Union[Dict, List]:
        """
        Read JSON file

        Args:
            file_name: Name of the JSON file
            encoding: File encoding (default: utf-8)

        Returns:
            Parsed JSON data (dict or list)
        """
        file_path = self.base_path / file_name

        try:
            if not file_path.exists():
                raise FileNotFoundError(f"JSON file not found: {file_path}")

            with open(file_path, 'r', encoding=encoding) as f:
                data = json.load(f)

            logger.info(f"Successfully read JSON file: {file_name}")
            return data

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in file {file_name}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error reading JSON file {file_name}: {str(e)}")
            raise

    def write_json(self, file_name: str, data: Union[Dict, List],
                   indent: int = 4, encoding: str = 'utf-8',
                   ensure_ascii: bool = False, sort_keys: bool = False) -> bool:
        """
        Write data to JSON file

        Args:
            file_name: Name of the JSON file
            data: Data to write (dict or list)
            indent: JSON indentation (default: 4)
            encoding: File encoding
            ensure_ascii: Escape non-ASCII characters
            sort_keys: Sort dictionary keys

        Returns:
            True if successful, False otherwise
        """
        file_path = self.base_path / file_name

        try:
            # Create directory if it doesn't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, 'w', encoding=encoding) as f:
                json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii,
                          sort_keys=sort_keys)

            logger.info(f"Successfully wrote JSON file: {file_name}")
            return True

        except Exception as e:
            logger.error(f"Error writing JSON file {file_name}: {str(e)}")
            return False

    def read_json_string(self, json_string: str) -> Union[Dict, List]:
        """
        Parse JSON string

        Args:
            json_string: JSON string

        Returns:
            Parsed JSON data
        """
        try:
            data = json.loads(json_string)
            logger.info("Successfully parsed JSON string")
            return data
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON string: {str(e)}")
            raise

    def to_json_string(self, data: Union[Dict, List], indent: int = 4,
                       ensure_ascii: bool = False, sort_keys: bool = False) -> str:
        """
        Convert data to JSON string

        Args:
            data: Data to convert
            indent: JSON indentation
            ensure_ascii: Escape non-ASCII characters
            sort_keys: Sort dictionary keys

        Returns:
            JSON string
        """
        try:
            json_string = json.dumps(data, indent=indent, ensure_ascii=ensure_ascii,
                                     sort_keys=sort_keys)
            logger.info("Successfully converted data to JSON string")
            return json_string
        except Exception as e:
            logger.error(f"Error converting to JSON string: {str(e)}")
            raise

    def pretty_print(self, data: Union[Dict, List], indent: int = 4) -> str:
        """
        Pretty print JSON data

        Args:
            data: Data to print
            indent: Indentation spaces

        Returns:
            Pretty formatted JSON string
        """
        try:
            formatted = json.dumps(data, indent=indent, ensure_ascii=False, sort_keys=False)
            print(formatted)
            return formatted
        except Exception as e:
            logger.error(f"Error pretty printing JSON: {str(e)}")
            raise

    def minify_json(self, data: Union[Dict, List]) -> str:
        """
        Minify JSON data (remove whitespace)

        Args:
            data: Data to minify

        Returns:
            Minified JSON string
        """
        try:
            minified = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
            logger.info("JSON data minified")
            return minified
        except Exception as e:
            logger.error(f"Error minifying JSON: {str(e)}")
            raise

    # ==================== Value Operations ====================

    def get_value(self, data: Union[Dict, List], key_path: str,
                  default: Any = None) -> Any:
        """
        Get value from JSON using dot notation path

        Args:
            data: JSON data
            key_path: Path in dot notation (e.g., 'user.address.city')
            default: Default value if path not found

        Returns:
            Value at the specified path or default
        """
        try:
            keys = key_path.split('.')
            value = data

            for key in keys:
                # Handle array index
                if '[' in key and ']' in key:
                    key_name = key[:key.index('[')]
                    index = int(key[key.index('[') + 1:key.index(']')])

                    if key_name:
                        value = value[key_name][index]
                    else:
                        value = value[index]
                else:
                    value = value[key]

            logger.info(f"Got value for path '{key_path}': {value}")
            return value

        except (KeyError, IndexError, TypeError) as e:
            logger.warning(f"Path '{key_path}' not found, returning default: {default}")
            return default

    def set_value(self, data: Union[Dict, List], key_path: str, value: Any) -> Union[Dict, List]:
        """
        Set value in JSON using dot notation path

        Args:
            data: JSON data
            key_path: Path in dot notation
            value: Value to set

        Returns:
            Modified JSON data
        """
        try:
            keys = key_path.split('.')
            current = data

            for i, key in enumerate(keys[:-1]):
                # Handle array index
                if '[' in key and ']' in key:
                    key_name = key[:key.index('[')]
                    index = int(key[key.index('[') + 1:key.index(']')])

                    if key_name:
                        current = current[key_name][index]
                    else:
                        current = current[index]
                else:
                    if key not in current:
                        current[key] = {}
                    current = current[key]

            # Set the final value
            final_key = keys[-1]
            if '[' in final_key and ']' in final_key:
                key_name = final_key[:final_key.index('[')]
                index = int(final_key[final_key.index('[') + 1:final_key.index(']')])

                if key_name:
                    current[key_name][index] = value
                else:
                    current[index] = value
            else:
                current[final_key] = value

            logger.info(f"Set value for path '{key_path}'")
            return data

        except Exception as e:
            logger.error(f"Error setting value for path '{key_path}': {str(e)}")
            raise

    def delete_key(self, data: Union[Dict, List], key_path: str) -> Union[Dict, List]:
        """
        Delete key from JSON using dot notation path

        Args:
            data: JSON data
            key_path: Path in dot notation

        Returns:
            Modified JSON data
        """
        try:
            keys = key_path.split('.')
            current = data

            for key in keys[:-1]:
                if '[' in key and ']' in key:
                    key_name = key[:key.index('[')]
                    index = int(key[key.index('[') + 1:key.index(']')])
                    current = current[key_name][index] if key_name else current[index]
                else:
                    current = current[key]

            # Delete the final key
            final_key = keys[-1]
            if '[' in final_key and ']' in final_key:
                key_name = final_key[:final_key.index('[')]
                index = int(final_key[final_key.index('[') + 1:final_key.index(']')])

                if key_name:
                    del current[key_name][index]
                else:
                    del current[index]
            else:
                del current[final_key]

            logger.info(f"Deleted key at path '{key_path}'")
            return data

        except Exception as e:
            logger.error(f"Error deleting key at path '{key_path}': {str(e)}")
            raise

    def has_key(self, data: Union[Dict, List], key_path: str) -> bool:
        """
        Check if key exists in JSON

        Args:
            data: JSON data
            key_path: Path in dot notation

        Returns:
            True if key exists, False otherwise
        """
        try:
            self.get_value(data, key_path)
            return True
        except:
            return False

    def get_keys(self, data: Dict, recursive: bool = False,
                 prefix: str = '') -> List[str]:
        """
        Get all keys from JSON

        Args:
            data: JSON data (dict)
            recursive: Get nested keys recursively
            prefix: Prefix for nested keys

        Returns:
            List of keys
        """
        keys = []

        if not isinstance(data, dict):
            return keys

        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            keys.append(full_key)

            if recursive and isinstance(value, dict):
                keys.extend(self.get_keys(value, recursive=True, prefix=full_key))
            elif recursive and isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        keys.extend(self.get_keys(item, recursive=True,
                                                  prefix=f"{full_key}[{i}]"))

        return keys

    # ==================== JSONPath Operations ====================

    def jsonpath_get(self, data: Union[Dict, List], jsonpath: str) -> List[Any]:
        """
        Get values using JSONPath expression

        Args:
            data: JSON data
            jsonpath: JSONPath expression (e.g., '$.user.address.city')

        Returns:
            List of matching values
        """
        try:
            jsonpath_expr = parser.parse(jsonpath)
            matches = [match.value for match in jsonpath_expr.find(data)]

            logger.info(f"JSONPath '{jsonpath}' found {len(matches)} matches")
            return matches

        except Exception as e:
            logger.error(f"Error in JSONPath query: {str(e)}")
            raise

    def jsonpath_set(self, data: Union[Dict, List], jsonpath: str, value: Any) -> Union[Dict, List]:
        """
        Set values using JSONPath expression

        Args:
            data: JSON data
            jsonpath: JSONPath expression
            value: Value to set

        Returns:
            Modified JSON data
        """
        try:
            jsonpath_expr = parser.parse(jsonpath)
            jsonpath_expr.update(data, value)

            logger.info(f"Updated values for JSONPath: {jsonpath}")
            return data

        except Exception as e:
            logger.error(f"Error setting value with JSONPath: {str(e)}")
            raise

    def jsonpath_delete(self, data: Union[Dict, List], jsonpath: str) -> Union[Dict, List]:
        """
        Delete values using JSONPath expression

        Args:
            data: JSON data
            jsonpath: JSONPath expression

        Returns:
            Modified JSON data
        """
        try:
            jsonpath_expr = parser.parse(jsonpath)
            matches = jsonpath_expr.find(data)

            # Delete matches in reverse order to avoid index issues
            for match in reversed(matches):
                if isinstance(match.context.value, dict):
                    del match.context.value[match.path.fields[0]]
                elif isinstance(match.context.value, list):
                    match.context.value.remove(match.value)

            logger.info(f"Deleted values for JSONPath: {jsonpath}")
            return data

        except Exception as e:
            logger.error(f"Error deleting with JSONPath: {str(e)}")
            raise

    # ==================== Schema Validation ====================

    def validate_schema(self, data: Union[Dict, List], schema: Dict) -> Tuple[bool, Optional[str]]:
        """
        Validate JSON data against schema

        Args:
            data: JSON data to validate
            schema: JSON schema

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            validate(instance=data, schema=schema)
            logger.info("JSON schema validation passed")
            return True, None
        except ValidationError as e:
            error_msg = f"Validation error: {e.message}"
            logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Schema validation error: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

    def validate_schema_file(self, data: Union[Dict, List], schema_file: str) -> Tuple[bool, Optional[str]]:
        """
        Validate JSON data against schema file

        Args:
            data: JSON data to validate
            schema_file: Path to schema file

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            schema = self.read_json(schema_file)
            return self.validate_schema(data, schema)
        except Exception as e:
            error_msg = f"Error loading schema file: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

    def get_schema_errors(self, data: Union[Dict, List], schema: Dict) -> List[str]:
        """
        Get all schema validation errors

        Args:
            data: JSON data to validate
            schema: JSON schema

        Returns:
            List of error messages
        """
        validator = Draft7Validator(schema)
        errors = [error.message for error in validator.iter_errors(data)]

        if errors:
            logger.warning(f"Found {len(errors)} schema validation errors")
        else:
            logger.info("No schema validation errors found")

        return errors

    # ==================== Comparison Operations ====================

    def compare_json(self, json1: Union[Dict, List], json2: Union[Dict, List]) -> Dict[str, Any]:
        """
        Compare two JSON objects

        Args:
            json1: First JSON object
            json2: Second JSON object

        Returns:
            Dictionary with comparison results
        """
        try:
            diff = jsondiff.diff(json1, json2)

            comparison = {
                'are_equal': len(diff) == 0,
                'differences': diff,
                'added': {},
                'removed': {},
                'changed': {}
            }

            if isinstance(diff, dict):
                for key, value in diff.items():
                    if isinstance(value, jsondiff.symbols.Symbol):
                        if str(value) == 'delete':
                            comparison['removed'][key] = json1.get(key)
                        elif str(value) == 'insert':
                            comparison['added'][key] = json2.get(key)
                    else:
                        comparison['changed'][key] = value

            logger.info(f"JSON comparison completed. Are equal: {comparison['are_equal']}")
            return comparison

        except Exception as e:
            logger.error(f"Error comparing JSON: {str(e)}")
            raise

    def deep_equal(self, json1: Union[Dict, List], json2: Union[Dict, List]) -> bool:
        """
        Check if two JSON objects are deeply equal

        Args:
            json1: First JSON object
            json2: Second JSON object

        Returns:
            True if equal, False otherwise
        """
        try:
            result = json1 == json2
            logger.info(f"Deep equal comparison: {result}")
            return result
        except Exception as e:
            logger.error(f"Error in deep equal comparison: {str(e)}")
            return False

    def generate_patch(self, source: Union[Dict, List],
                       target: Union[Dict, List]) -> List[Dict]:
        """
        Generate JSON patch to transform source to target

        Args:
            source: Source JSON object
            target: Target JSON object

        Returns:
            JSON patch as list of operations
        """
        try:
            patch = jsonpatch.make_patch(source, target)
            logger.info(f"Generated JSON patch with {len(patch.patch)} operations")
            return patch.patch
        except Exception as e:
            logger.error(f"Error generating JSON patch: {str(e)}")
            raise

    def apply_patch(self, data: Union[Dict, List], patch: List[Dict]) -> Union[Dict, List]:
        """
        Apply JSON patch to data

        Args:
            data: JSON data
            patch: JSON patch operations

        Returns:
            Patched JSON data
        """
        try:
            patch_obj = jsonpatch.JsonPatch(patch)
            result = patch_obj.apply(data)
            logger.info("JSON patch applied successfully")
            return result
        except Exception as e:
            logger.error(f"Error applying JSON patch: {str(e)}")
            raise

    # ==================== Transformation Operations ====================

    def merge_json(self, *json_objects: Union[Dict, List],
                   deep: bool = True) -> Union[Dict, List]:
        """
        Merge multiple JSON objects

        Args:
            *json_objects: JSON objects to merge
            deep: Perform deep merge

        Returns:
            Merged JSON object
        """
        try:
            if not json_objects:
                return {}

            result = copy.deepcopy(json_objects[0])

            for obj in json_objects[1:]:
                if deep:
                    result = self._deep_merge(result, obj)
                else:
                    result.update(obj)

            logger.info(f"Merged {len(json_objects)} JSON objects")
            return result

        except Exception as e:
            logger.error(f"Error merging JSON: {str(e)}")
            raise

    def _deep_merge(self, dict1: Dict, dict2: Dict) -> Dict:
        """
        Deep merge two dictionaries

        Args:
            dict1: First dictionary
            dict2: Second dictionary

        Returns:
            Merged dictionary
        """
        result = copy.deepcopy(dict1)

        for key, value in dict2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = copy.deepcopy(value)

        return result

    def flatten_json(self, data: Union[Dict, List], separator: str = '.') -> Dict:
        """
        Flatten nested JSON to single level

        Args:
            data: JSON data to flatten
            separator: Separator for nested keys

        Returns:
            Flattened dictionary
        """

        def _flatten(obj, parent_key=''):
            items = []

            if isinstance(obj, dict):
                for key, value in obj.items():
                    new_key = f"{parent_key}{separator}{key}" if parent_key else key
                    items.extend(_flatten(value, new_key).items())
            elif isinstance(obj, list):
                for i, value in enumerate(obj):
                    new_key = f"{parent_key}[{i}]"
                    items.extend(_flatten(value, new_key).items())
            else:
                items.append((parent_key, obj))

            return dict(items)

        try:
            flattened = _flatten(data)
            logger.info(f"Flattened JSON to {len(flattened)} keys")
            return flattened
        except Exception as e:
            logger.error(f"Error flattening JSON: {str(e)}")
            raise

    def unflatten_json(self, data: Dict, separator: str = '.') -> Union[Dict, List]:
        """
        Unflatten single-level JSON to nested structure

        Args:
            data: Flattened JSON data
            separator: Separator used in keys

        Returns:
            Nested JSON structure
        """
        try:
            result = {}

            for key, value in data.items():
                parts = key.split(separator)
                current = result

                for i, part in enumerate(parts[:-1]):
                    # Handle array notation
                    if '[' in part:
                        array_key = part[:part.index('[')]
                        index = int(part[part.index('[') + 1:part.index(']')])

                        if array_key not in current:
                            current[array_key] = []

                        while len(current[array_key]) <= index:
                            current[array_key].append({})

                        current = current[array_key][index]
                    else:
                        if part not in current:
                            current[part] = {}
                        current = current[part]

                # Set the final value
                final_key = parts[-1]
                if '[' in final_key:
                    array_key = final_key[:final_key.index('[')]
                    index = int(final_key[final_key.index('[') + 1:final_key.index(']')])

                    if array_key not in current:
                        current[array_key] = []

                    while len(current[array_key]) <= index:
                        current[array_key].append(None)

                    current[array_key][index] = value
                else:
                    current[final_key] = value

            logger.info("Unflattened JSON successfully")
            return result

        except Exception as e:
            logger.error(f"Error unflattening JSON: {str(e)}")
            raise

    def filter_keys(self, data: Dict, keys: List[str], include: bool = True) -> Dict:
        """
        Filter JSON by keys

        Args:
            data: JSON data
            keys: List of keys to include/exclude
            include: True to include keys, False to exclude

        Returns:
            Filtered JSON data
        """
        try:
            if include:
                filtered = {k: v for k, v in data.items() if k in keys}
            else:
                filtered = {k: v for k, v in data.items() if k not in keys}

            logger.info(f"Filtered JSON: {len(filtered)} keys remaining")
            return filtered

        except Exception as e:
            logger.error(f"Error filtering JSON: {str(e)}")
            raise

    def sort_keys(self, data: Union[Dict, List], reverse: bool = False) -> Union[Dict, List]:
        """
        Sort JSON keys recursively

        Args:
            data: JSON data
            reverse: Sort in reverse order

        Returns:
            JSON with sorted keys
        """
        try:
            if isinstance(data, dict):
                return {k: self.sort_keys(v, reverse)
                        for k, v in sorted(data.items(), reverse=reverse)}
            elif isinstance(data, list):
                return [self.sort_keys(item, reverse) for item in data]
            else:
                return data
        except Exception as e:
            logger.error(f"Error sorting JSON keys: {str(e)}")
            raise

    # ==================== Search Operations ====================

    def search_by_key(self, data: Union[Dict, List], search_key: str) -> List[Any]:
        """
        Search for all values with matching key

        Args:
            data: JSON data
            search_key: Key to search for

        Returns:
            List of matching values
        """
        results = []

        def _search(obj):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if key == search_key:
                        results.append(value)
                    _search(value)
            elif isinstance(obj, list):
                for item in obj:
                    _search(item)

        try:
            _search(data)
            logger.info(f"Found {len(results)} values for key '{search_key}'")
            return results
        except Exception as e:
            logger.error(f"Error searching by key: {str(e)}")
            return []

    def search_by_value(self, data: Union[Dict, List], search_value: Any) -> List[str]:
        """
        Search for all keys with matching value

        Args:
            data: JSON data
            search_value: Value to search for

        Returns:
            List of matching key paths
        """
        results = []

        def _search(obj, path=''):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    new_path = f"{path}.{key}" if path else key
                    if value == search_value:
                        results.append(new_path)
                    _search(value, new_path)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    new_path = f"{path}[{i}]"
                    if item == search_value:
                        results.append(new_path)
                    _search(item, new_path)

        try:
            _search(data)
            logger.info(f"Found {len(results)} keys for value '{search_value}'")
            return results
        except Exception as e:
            logger.error(f"Error searching by value: {str(e)}")
            return []

    def search_by_pattern(self, data: Union[Dict, List], pattern: str,
                          search_keys: bool = True, search_values: bool = True) -> Dict[str, List]:
        """
        Search using regex pattern

        Args:
            data: JSON data
            pattern: Regex pattern
            search_keys: Search in keys
            search_values: Search in values

        Returns:
            Dictionary with 'keys' and 'values' lists of matches
        """
        import re

        regex = re.compile(pattern)
        results = {'keys': [], 'values': []}

        def _search(obj, path=''):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    new_path = f"{path}.{key}" if path else key

                    if search_keys and regex.search(str(key)):
                        results['keys'].append(new_path)

                    if search_values and isinstance(value, str) and regex.search(value):
                        results['values'].append({'path': new_path, 'value': value})

                    _search(value, new_path)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    new_path = f"{path}[{i}]"

                    if search_values and isinstance(item, str) and regex.search(item):
                        results['values'].append({'path': new_path, 'value': item})

                    _search(item, new_path)

        try:
            _search(data)
            logger.info(f"Pattern search found {len(results['keys'])} keys and "
                        f"{len(results['values'])} values")
            return results
        except Exception as e:
            logger.error(f"Error searching by pattern: {str(e)}")
            return {'keys': [], 'values': []}

    # ==================== Utility Operations ====================

    def get_size(self, data: Union[Dict, List]) -> int:
        """
        Get size of JSON data in bytes

        Args:
            data: JSON data

        Returns:
            Size in bytes
        """
        try:
            json_string = json.dumps(data)
            size = len(json_string.encode('utf-8'))
            logger.info(f"JSON size: {size} bytes")
            return size
        except Exception as e:
            logger.error(f"Error getting JSON size: {str(e)}")
            return 0

    def get_depth(self, data: Union[Dict, List]) -> int:
        """
        Get maximum depth of JSON structure

        Args:
            data: JSON data

        Returns:
            Maximum depth
        """

        def _get_depth(obj, current_depth=0):
            if isinstance(obj, dict):
                if not obj:
                    return current_depth
                return max(_get_depth(v, current_depth + 1) for v in obj.values())
            elif isinstance(obj, list):
                if not obj:
                    return current_depth
                return max(_get_depth(item, current_depth + 1) for item in obj)
            else:
                return current_depth

        try:
            depth = _get_depth(data)
            logger.info(f"JSON depth: {depth}")
            return depth
        except Exception as e:
            logger.error(f"Error getting JSON depth: {str(e)}")
            return 0

    def count_elements(self, data: Union[Dict, List]) -> Dict[str, int]:
        """
        Count total elements in JSON

        Args:
            data: JSON data

        Returns:
            Dictionary with counts by type
        """
        counts = {'objects': 0, 'arrays': 0, 'strings': 0, 'numbers': 0,
                  'booleans': 0, 'nulls': 0, 'total': 0}

        def _count(obj):
            counts['total'] += 1

            if isinstance(obj, dict):
                counts['objects'] += 1
                for value in obj.values():
                    _count(value)
            elif isinstance(obj, list):
                counts['arrays'] += 1
                for item in obj:
                    _count(item)
            elif isinstance(obj, str):
                counts['strings'] += 1
            elif isinstance(obj, (int, float)):
                counts['numbers'] += 1
            elif isinstance(obj, bool):
                counts['booleans'] += 1
            elif obj is None:
                counts['nulls'] += 1

        try:
            _count(data)
            logger.info(f"Element count: {counts}")
            return counts
        except Exception as e:
            logger.error(f"Error counting elements: {str(e)}")
            return counts

    def copy_json(self, data: Union[Dict, List], deep: bool = True) -> Union[Dict, List]:
        """
        Copy JSON data

        Args:
            data: JSON data to copy
            deep: Perform deep copy

        Returns:
            Copied JSON data
        """
        try:
            if deep:
                copied = copy.deepcopy(data)
            else:
                copied = copy.copy(data)

            logger.info("JSON data copied")
            return copied
        except Exception as e:
            logger.error(f"Error copying JSON: {str(e)}")
            raise

    def is_valid_json(self, json_string: str) -> bool:
        """
        Check if string is valid JSON

        Args:
            json_string: JSON string to validate

        Returns:
            True if valid, False otherwise
        """
        try:
            json.loads(json_string)
            logger.info("Valid JSON string")
            return True
        except json.JSONDecodeError:
            logger.info("Invalid JSON string")
            return False

    def sanitize_json(self, data: Union[Dict, List],
                      remove_nulls: bool = True,
                      remove_empty_strings: bool = True,
                      remove_empty_collections: bool = True) -> Union[Dict, List]:
        """
        Sanitize JSON by removing unwanted values

        Args:
            data: JSON data
            remove_nulls: Remove null values
            remove_empty_strings: Remove empty strings
            remove_empty_collections: Remove empty arrays/objects

        Returns:
            Sanitized JSON data
        """

        def _sanitize(obj):
            if isinstance(obj, dict):
                sanitized = {}
                for key, value in obj.items():
                    cleaned_value = _sanitize(value)

                    # Skip based on conditions
                    if remove_nulls and cleaned_value is None:
                        continue
                    if remove_empty_strings and cleaned_value == '':
                        continue
                    if remove_empty_collections and cleaned_value in ({}, []):
                        continue

                    sanitized[key] = cleaned_value

                return sanitized

            elif isinstance(obj, list):
                sanitized = []
                for item in obj:
                    cleaned_item = _sanitize(item)

                    # Skip based on conditions
                    if remove_nulls and cleaned_item is None:
                        continue
                    if remove_empty_strings and cleaned_item == '':
                        continue
                    if remove_empty_collections and cleaned_item in ({}, []):
                        continue

                    sanitized.append(cleaned_item)

                return sanitized

            else:
                return obj

        try:
            sanitized = _sanitize(data)
            logger.info("JSON data sanitized")
            return sanitized
        except Exception as e:
            logger.error(f"Error sanitizing JSON: {str(e)}")
            raise

        # ==================== Type Conversion ====================

    def to_xml(self, data: Union[Dict, List], root_tag: str = 'root') -> str:
        """
        Convert JSON to XML string

        Args:
            data: JSON data
            root_tag: Root XML tag name

        Returns:
            XML string
        """
        try:
            import xmltodict

            xml_string = xmltodict.unparse({root_tag: data}, pretty=True)
            logger.info("Converted JSON to XML")
            return xml_string
        except Exception as e:
            logger.error(f"Error converting JSON to XML: {str(e)}")
            raise

    def to_yaml(self, data: Union[Dict, List]) -> str:
        """
        Convert JSON to YAML string

        Args:
            data: JSON data

        Returns:
            YAML string
        """
        try:
            import yaml

            yaml_string = yaml.dump(data, default_flow_style=False, allow_unicode=True)
            logger.info("Converted JSON to YAML")
            return yaml_string
        except Exception as e:
            logger.error(f"Error converting JSON to YAML: {str(e)}")
            raise

    def to_csv(self, data: List[Dict], output_file: str = None) -> str:
        """
        Convert JSON array to CSV

        Args:
            data: List of JSON objects (with consistent keys)
            output_file: Optional output file name

        Returns:
            CSV string
        """
        try:
            import csv
            import io

            if not data or not isinstance(data, list):
                raise ValueError("Data must be a non-empty list of dictionaries")

            output = io.StringIO()

            # Get all unique keys
            keys = set()
            for item in data:
                if isinstance(item, dict):
                    keys.update(item.keys())

            keys = sorted(keys)

            writer = csv.DictWriter(output, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)

            csv_string = output.getvalue()
            output.close()

            # Save to file if specified
            if output_file:
                csv_path = self.base_path.parent / "csv" / output_file
                csv_path.parent.mkdir(parents=True, exist_ok=True)
                with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                    f.write(csv_string)
                logger.info(f"Saved CSV to: {csv_path}")

            logger.info("Converted JSON to CSV")
            return csv_string

        except Exception as e:
            logger.error(f"Error converting JSON to CSV: {str(e)}")
            raise

        # ==================== Template and Replacement ====================

    def replace_placeholders(self, data: Union[Dict, List],
                             replacements: Dict[str, Any],
                             placeholder_pattern: str = r'\{\{(\w+)\}\}') -> Union[Dict, List]:
        """
        Replace placeholders in JSON with actual values

        Args:
            data: JSON data with placeholders
            replacements: Dictionary of placeholder:value pairs
            placeholder_pattern: Regex pattern for placeholders

        Returns:
            JSON data with replaced values
        """
        import re

        def _replace(obj):
            if isinstance(obj, dict):
                return {key: _replace(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [_replace(item) for item in obj]
            elif isinstance(obj, str):
                # Replace all placeholders in the string
                def replace_match(match):
                    placeholder = match.group(1)
                    return str(replacements.get(placeholder, match.group(0)))

                return re.sub(placeholder_pattern, replace_match, obj)
            else:
                return obj

        try:
            replaced = _replace(data)
            logger.info(f"Replaced placeholders with {len(replacements)} values")
            return replaced
        except Exception as e:
            logger.error(f"Error replacing placeholders: {str(e)}")
            raise

    def create_template(self, data: Union[Dict, List],
                        keys_to_template: List[str]) -> Union[Dict, List]:
        """
        Create template from JSON by replacing values with placeholders

        Args:
            data: JSON data
            keys_to_template: List of keys to convert to placeholders

        Returns:
            Template JSON with placeholders
        """

        def _templatize(obj, path=''):
            if isinstance(obj, dict):
                result = {}
                for key, value in obj.items():
                    full_path = f"{path}.{key}" if path else key

                    if key in keys_to_template or full_path in keys_to_template:
                        result[key] = f"{{{{{key}}}}}"
                    else:
                        result[key] = _templatize(value, full_path)

                return result

            elif isinstance(obj, list):
                return [_templatize(item, f"{path}[{i}]") for i, item in enumerate(obj)]

            else:
                return obj

        try:
            template = _templatize(data)
            logger.info(f"Created template for {len(keys_to_template)} keys")
            return template
        except Exception as e:
            logger.error(f"Error creating template: {str(e)}")
            raise

        # ==================== Batch Operations ====================

    def batch_read(self, file_names: List[str]) -> Dict[str, Union[Dict, List]]:
        """
        Read multiple JSON files

        Args:
            file_names: List of file names

        Returns:
            Dictionary mapping file names to their data
        """
        results = {}

        for file_name in file_names:
            try:
                results[file_name] = self.read_json(file_name)
            except Exception as e:
                logger.error(f"Error reading {file_name}: {str(e)}")
                results[file_name] = None

        logger.info(f"Batch read {len(results)} files")
        return results

    def batch_write(self, data_dict: Dict[str, Union[Dict, List]], **kwargs) -> Dict[str, bool]:
        """
        Write multiple JSON files

        Args:
            data_dict: Dictionary mapping file names to data
            **kwargs: Additional arguments for write_json

        Returns:
            Dictionary mapping file names to success status
        """
        results = {}

        for file_name, data in data_dict.items():
            try:
                results[file_name] = self.write_json(file_name, data, **kwargs)
            except Exception as e:
                logger.error(f"Error writing {file_name}: {str(e)}")
                results[file_name] = False

        logger.info(f"Batch wrote {len(results)} files")
        return results

        # ==================== Test Data Generation ====================

    def generate_test_data(self, schema: Dict, count: int = 1) -> List[Dict]:
        """
        Generate test data based on schema

        Args:
            schema: JSON schema
            count: Number of test data instances to generate

        Returns:
            List of generated test data
        """
        from faker import Faker
        fake = Faker()

        def _generate_value(schema_type, schema_format=None):
            if schema_type == 'string':
                if schema_format == 'email':
                    return fake.email()
                elif schema_format == 'date':
                    return fake.date()
                elif schema_format == 'date-time':
                    return fake.iso8601()
                else:
                    return fake.word()
            elif schema_type == 'integer':
                return fake.random_int(min=0, max=1000)
            elif schema_type == 'number':
                return fake.random.uniform(0, 1000)
            elif schema_type == 'boolean':
                return fake.boolean()
            elif schema_type == 'null':
                return None
            else:
                return None

        def _generate_object(schema_def):
            obj = {}
            properties = schema_def.get('properties', {})

            for key, prop_schema in properties.items():
                prop_type = prop_schema.get('type')
                prop_format = prop_schema.get('format')

                if prop_type == 'object':
                    obj[key] = _generate_object(prop_schema)
                elif prop_type == 'array':
                    items_schema = prop_schema.get('items', {})
                    obj[key] = [_generate_value(items_schema.get('type')) for _ in range(3)]
                else:
                    obj[key] = _generate_value(prop_type, prop_format)

            return obj

        try:
            test_data = [_generate_object(schema) for _ in range(count)]
            logger.info(f"Generated {count} test data instances")
            return test_data
        except Exception as e:
            logger.error(f"Error generating test data: {str(e)}")
            raise

        # ==================== Statistics ====================

    def get_statistics(self, data: Union[Dict, List]) -> Dict[str, Any]:
        """
        Get comprehensive statistics about JSON data

        Args:
            data: JSON data

        Returns:
            Dictionary with statistics
        """
        try:
            stats = {
                'size_bytes': self.get_size(data),
                'depth': self.get_depth(data),
                'element_counts': self.count_elements(data),
                'total_keys': len(self.get_keys(data, recursive=True)) if isinstance(data, dict) else 0,
                'is_array': isinstance(data, list),
                'is_object': isinstance(data, dict),
                'array_length': len(data) if isinstance(data, list) else None
            }

            logger.info("Statistics generated")
            return stats

        except Exception as e:
            logger.error(f"Error getting statistics: {str(e)}")
            return {}
