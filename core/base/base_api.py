"""
Base API Service class
Provides common API functionalities for all API service classes

File: framework/base/base_api.py
Author: Automation Team
Description: Base class for all API service classes with comprehensive HTTP methods,
             validation, authentication, and reporting capabilities.
"""

import logging
import allure
from typing import Dict, Any, Optional, List
from core.utils.api_client_utility import APIClientUtility
from core.utils.json_utility import JSONUtility
import requests
import json
import time
import statistics


class BaseAPIService:
    """
    Base API service class providing common API functionalities
    All API service classes should inherit from this class

    Features:
    - All HTTP methods (GET, POST, PUT, PATCH, DELETE)
    - Request/Response validation
    - JSON schema validation
    - Authentication (Basic, Bearer, API Key)
    - Response extraction and manipulation
    - Batch operations
    - Performance testing
    - Allure report integration
    - Comprehensive logging
    """

    def __init__(self, api_client: APIClientUtility):
        """
        Initialize base API service

        Args:
            api_client: APIClientUtility instance for making HTTP requests
        """
        self.api_client = api_client
        self.json_utility = JSONUtility()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.last_response = None
        self.last_request = None

    # ========================================================================
    # HTTP REQUEST METHODS
    # ========================================================================

    @allure.step("GET request to: {endpoint}")
    def get_request(self, endpoint: str, params: Dict = None,
                    headers: Dict = None) -> requests.Response:
        """
        Make GET request

        Args:
            endpoint: API endpoint path
            params: Query parameters as dictionary
            headers: Additional headers to send

        Returns:
            requests.Response object

        Example:
            response = self.get_request("/users", params={"page": 1})
        """
        try:
            self.logger.info(f"GET request to: {endpoint}")
            if params:
                self.logger.debug(f"Parameters: {params}")

            response = self.api_client.get(endpoint, params=params, headers=headers)
            self.last_response = response

            self._log_response(response)
            self._attach_response_to_allure(response)

            return response

        except Exception as e:
            self.logger.error(f"GET request failed: {e}")
            raise

    @allure.step("POST request to: {endpoint}")
    def post_request(self, endpoint: str, payload: Dict = None,
                     headers: Dict = None, files: Dict = None) -> requests.Response:
        """
        Make POST request

        Args:
            endpoint: API endpoint path
            payload: Request payload/body as dictionary
            headers: Additional headers to send
            files: Files to upload as dictionary

        Returns:
            requests.Response object

        Example:
            payload = {"name": "John", "email": "john@example.com"}
            response = self.post_request("/users", payload=payload)
        """
        try:
            self.logger.info(f"POST request to: {endpoint}")
            if payload:
                self.logger.debug(f"Payload: {payload}")

            self._attach_request_to_allure(payload)

            response = self.api_client.post(
                endpoint,
                json_data=payload,
                headers=headers,
                files=files
            )
            self.last_response = response
            self.last_request = payload

            self._log_response(response)
            self._attach_response_to_allure(response)

            return response

        except Exception as e:
            self.logger.error(f"POST request failed: {e}")
            raise

    @allure.step("PUT request to: {endpoint}")
    def put_request(self, endpoint: str, payload: Dict = None,
                    headers: Dict = None) -> requests.Response:
        """
        Make PUT request

        Args:
            endpoint: API endpoint path
            payload: Request payload/body as dictionary
            headers: Additional headers to send

        Returns:
            requests.Response object

        Example:
            payload = {"name": "John Updated"}
            response = self.put_request("/users/1", payload=payload)
        """
        try:
            self.logger.info(f"PUT request to: {endpoint}")
            if payload:
                self.logger.debug(f"Payload: {payload}")

            self._attach_request_to_allure(payload)

            response = self.api_client.put(endpoint, json_data=payload, headers=headers)
            self.last_response = response
            self.last_request = payload

            self._log_response(response)
            self._attach_response_to_allure(response)

            return response

        except Exception as e:
            self.logger.error(f"PUT request failed: {e}")
            raise

    @allure.step("PATCH request to: {endpoint}")
    def patch_request(self, endpoint: str, payload: Dict = None,
                      headers: Dict = None) -> requests.Response:
        """
        Make PATCH request

        Args:
            endpoint: API endpoint path
            payload: Request payload/body as dictionary
            headers: Additional headers to send

        Returns:
            requests.Response object

        Example:
            payload = {"email": "newemail@example.com"}
            response = self.patch_request("/users/1", payload=payload)
        """
        try:
            self.logger.info(f"PATCH request to: {endpoint}")
            if payload:
                self.logger.debug(f"Payload: {payload}")

            self._attach_request_to_allure(payload)

            response = self.api_client.patch(endpoint, json_data=payload, headers=headers)
            self.last_response = response
            self.last_request = payload

            self._log_response(response)
            self._attach_response_to_allure(response)

            return response

        except Exception as e:
            self.logger.error(f"PATCH request failed: {e}")
            raise

    @allure.step("DELETE request to: {endpoint}")
    def delete_request(self, endpoint: str, headers: Dict = None) -> requests.Response:
        """
        Make DELETE request

        Args:
            endpoint: API endpoint path
            headers: Additional headers to send

        Returns:
            requests.Response object

        Example:
            response = self.delete_request("/users/1")
        """
        try:
            self.logger.info(f"DELETE request to: {endpoint}")

            response = self.api_client.delete(endpoint, headers=headers)
            self.last_response = response

            self._log_response(response)
            self._attach_response_to_allure(response)

            return response

        except Exception as e:
            self.logger.error(f"DELETE request failed: {e}")
            raise

    # ========================================================================
    # VALIDATION METHODS
    # ========================================================================

    def validate_status_code(self, response: requests.Response, expected_status: int = 200):
        """
        Validate response status code

        Args:
            response: Response object to validate
            expected_status: Expected HTTP status code

        Raises:
            AssertionError: If status code doesn't match

        Example:
            self.validate_status_code(response, 201)
        """
        with allure.step(f"Validate status code is {expected_status}"):
            try:
                self.api_client.validate_response_status(response, expected_status)
                self.logger.info(f"[PASS] Status code validation passed: {response.status_code}")
            except AssertionError as e:
                self.logger.error(f"[FAIL] Status code validation failed: {e}")
                raise

    def validate_response_time(self, response: requests.Response, max_time: float = 5.0):
        """
        Validate response time is within acceptable limit

        Args:
            response: Response object to validate
            max_time: Maximum acceptable response time in seconds

        Raises:
            AssertionError: If response time exceeds max_time

        Example:
            self.validate_response_time(response, max_time=2.0)
        """
        with allure.step(f"Validate response time is less than {max_time}s"):
            try:
                self.api_client.validate_response_time(response, max_time)
                response_time = response.elapsed.total_seconds()
                self.logger.info(f"[PASS] Response time validation passed: {response_time:.3f}s")
            except AssertionError as e:
                self.logger.error(f"[FAIL] Response time validation failed: {e}")
                raise

    def validate_response_contains_key(self, response_data: Dict, key: str):
        """
        Validate that response contains a specific key

        Args:
            response_data: Response JSON data as dictionary
            key: Key name to check for

        Raises:
            AssertionError: If key is not found

        Example:
            self.validate_response_contains_key(response_data, "id")
        """
        with allure.step(f"Validate response contains key: {key}"):
            try:
                assert key in response_data, f"Key '{key}' not found in response"
                self.logger.info(f"[PASS] Response contains key: {key}")
            except AssertionError as e:
                self.logger.error(f"[FAIL] Key validation failed: {e}")
                raise

    def validate_response_value(self, response_data: Dict, key: str, expected_value: Any):
        """
        Validate response value for a specific key

        Args:
            response_data: Response JSON data as dictionary
            key: Key name to check
            expected_value: Expected value for the key

        Raises:
            AssertionError: If value doesn't match

        Example:
            self.validate_response_value(response_data, "status", "active")
        """
        with allure.step(f"Validate {key} equals {expected_value}"):
            try:
                actual_value = response_data.get(key)
                assert actual_value == expected_value, \
                    f"Expected {key}='{expected_value}', got '{actual_value}'"
                self.logger.info(f"[PASS] Value validation passed: {key}={expected_value}")
            except AssertionError as e:
                self.logger.error(f"[FAIL] Value validation failed: {e}")
                raise

    def validate_json_schema(self, response_data: Dict, schema_file: str):
        """
        Validate JSON response against schema file

        Args:
            response_data: Response JSON data as dictionary
            schema_file: Path to JSON schema file

        Raises:
            ValidationError: If schema validation fails

        Example:
            self.validate_json_schema(response_data, "framework/models/schemas/user_schema.json")
        """
        with allure.step(f"Validate JSON schema: {schema_file}"):
            try:
                schema = self.json_utility.read_json_file(schema_file)
                self.api_client.validate_json_schema(response_data, schema)
                self.logger.info("[PASS] JSON schema validation passed")
            except Exception as e:
                self.logger.error(f"[FAIL] JSON schema validation failed: {e}")
                raise

    def validate_response_not_empty(self, response_data: Any):
        """
        Validate that response is not empty

        Args:
            response_data: Response data to validate

        Raises:
            AssertionError: If response is empty

        Example:
            self.validate_response_not_empty(response_data)
        """
        with allure.step("Validate response is not empty"):
            try:
                assert response_data, "Response is empty"
                self.logger.info("[PASS] Response is not empty")
            except AssertionError as e:
                self.logger.error(f"[FAIL] Empty response validation failed: {e}")
                raise

    def validate_response_list_length(self, response_data: List, expected_length: int):
        """
        Validate response list has expected length

        Args:
            response_data: Response list to validate
            expected_length: Expected list length

        Raises:
            AssertionError: If list length doesn't match

        Example:
            self.validate_response_list_length(users_list, 10)
        """
        with allure.step(f"Validate list length is {expected_length}"):
            try:
                actual_length = len(response_data)
                assert actual_length == expected_length, \
                    f"Expected list length {expected_length}, got {actual_length}"
                self.logger.info(f"[PASS] List length validation passed: {actual_length}")
            except AssertionError as e:
                self.logger.error(f"[FAIL] List length validation failed: {e}")
                raise

    # ========================================================================
    # RESPONSE EXTRACTION METHODS
    # ========================================================================

    def extract_json_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Extract JSON from response

        Args:
            response: Response object

        Returns:
            JSON data as dictionary

        Raises:
            JSONDecodeError: If response is not valid JSON

        Example:
            response_data = self.extract_json_response(response)
        """
        with allure.step("Extract JSON response"):
            try:
                json_data = self.api_client.extract_json_response(response)
                self.logger.info("[PASS] Successfully extracted JSON response")
                return json_data
            except Exception as e:
                self.logger.error(f"[FAIL] JSON extraction failed: {e}")
                raise

    def extract_value_from_response(self, response_data: Dict, key_path: str) -> Any:
        """
        Extract value from nested JSON response using dot notation

        Args:
            response_data: Response JSON data as dictionary
            key_path: Key path using dot notation (e.g., "data.user.id")

        Returns:
            Extracted value

        Raises:
            KeyError: If key path is invalid

        Example:
            user_id = self.extract_value_from_response(response_data, "data.user.id")
        """
        try:
            keys = key_path.split('.')
            value = response_data

            for key in keys:
                if isinstance(value, list):
                    # Handle list indexing
                    key = int(key)
                value = value[key]

            self.logger.info(f"Extracted value from {key_path}: {value}")
            return value

        except (KeyError, TypeError, IndexError) as e:
            self.logger.error(f"Failed to extract value from {key_path}: {e}")
            raise

    def extract_all_values(self, response_data: List[Dict], key: str) -> List[Any]:
        """
        Extract all values for a specific key from list of dictionaries

        Args:
            response_data: List of dictionaries
            key: Key name to extract from each dictionary

        Returns:
            List of extracted values

        Example:
            user_ids = self.extract_all_values(users_list, "id")
        """
        try:
            values = [item.get(key) for item in response_data if isinstance(item, dict)]
            self.logger.info(f"Extracted {len(values)} values for key: {key}")
            return values
        except Exception as e:
            self.logger.error(f"Failed to extract all values: {e}")
            raise

    def extract_id_from_location_header(self, response: requests.Response) -> Optional[str]:
        """
        Extract ID from Location header (commonly used after POST requests)

        Args:
            response: Response object

        Returns:
            Extracted ID or None if not found

        Example:
            resource_id = self.extract_id_from_location_header(response)
        """
        try:
            location = response.headers.get('Location', '')
            if location:
                # Extract last part of URL (assuming it's the ID)
                resource_id = location.rstrip('/').split('/')[-1]
                self.logger.info(f"Extracted ID from Location header: {resource_id}")
                return resource_id
            return None
        except Exception as e:
            self.logger.error(f"Failed to extract ID from Location header: {e}")
            return None

    # ========================================================================
    # HEADER METHODS
    # ========================================================================

    def set_authorization_header(self, token: str, auth_type: str = "Bearer"):
        """
        Set authorization header

        Args:
            token: Authorization token
            auth_type: Type of authorization (Bearer, Basic, etc.)

        Example:
            self.set_authorization_header("your_token_here", "Bearer")
        """
        try:
            self.api_client.session.headers["Authorization"] = f"{auth_type} {token}"
            self.logger.info(f"Set authorization header: {auth_type}")
        except Exception as e:
            self.logger.error(f"Failed to set authorization header: {e}")
            raise

    def set_custom_header(self, key: str, value: str):
        """
        Set custom header

        Args:
            key: Header key/name
            value: Header value

        Example:
            self.set_custom_header("X-Custom-Header", "custom-value")
        """
        try:
            self.api_client.session.headers[key] = value
            self.logger.info(f"Set custom header: {key}={value}")
        except Exception as e:
            self.logger.error(f"Failed to set custom header: {e}")
            raise

    def remove_header(self, key: str):
        """
        Remove header from session

        Args:
            key: Header key to remove

        Example:
            self.remove_header("Authorization")
        """
        try:
            if key in self.api_client.session.headers:
                del self.api_client.session.headers[key]
                self.logger.info(f"Removed header: {key}")
        except Exception as e:
            self.logger.error(f"Failed to remove header: {e}")
            raise

    def get_response_headers(self, response: requests.Response) -> Dict:
        """
        Get all response headers

        Args:
            response: Response object

        Returns:
            Dictionary of response headers

        Example:
            headers = self.get_response_headers(response)
        """
        try:
            headers = dict(response.headers)
            self.logger.info(f"Retrieved {len(headers)} response headers")
            return headers
        except Exception as e:
            self.logger.error(f"Failed to get response headers: {e}")
            raise

    def get_response_header(self, response: requests.Response, header_name: str) -> Optional[str]:
        """
        Get specific response header value

        Args:
            response: Response object
            header_name: Name of the header

        Returns:
            Header value or None if not found

        Example:
            content_type = self.get_response_header(response, "Content-Type")
        """
        try:
            value = response.headers.get(header_name)
            self.logger.info(f"Header {header_name}: {value}")
            return value
        except Exception as e:
            self.logger.error(f"Failed to get response header: {e}")
            raise

    # ========================================================================
    # AUTHENTICATION METHODS
    # ========================================================================

    def login_with_basic_auth(self, username: str, password: str):
        """
        Set Basic authentication

        Args:
            username: Username for authentication
            password: Password for authentication

        Example:
            self.login_with_basic_auth("admin", "password123")
        """
        try:
            self.api_client.set_authentication("basic", username=username, password=password)
            self.logger.info("Basic authentication configured")
        except Exception as e:
            self.logger.error(f"Failed to set basic auth: {e}")
            raise

    def login_with_bearer_token(self, token: str):
        """
        Set Bearer token authentication

        Args:
            token: Bearer token for authentication

        Example:
            self.login_with_bearer_token("your_jwt_token_here")
        """
        try:
            self.api_client.set_authentication("bearer", token=token)
            self.logger.info("Bearer token authentication configured")
        except Exception as e:
            self.logger.error(f"Failed to set bearer token: {e}")
            raise

    def login_with_api_key(self, api_key: str, key_name: str = "X-API-Key"):
        """
        Set API key authentication

        Args:
            api_key: API key for authentication
            key_name: Header name for API key (default: X-API-Key)

        Example:
            self.login_with_api_key("your_api_key", "X-API-Key")
        """
        try:
            self.api_client.set_authentication("api_key", api_key=api_key, key_name=key_name)
            self.logger.info(f"API key authentication configured: {key_name}")
        except Exception as e:
            self.logger.error(f"Failed to set API key: {e}")
            raise

    # ========================================================================
    # BATCH OPERATIONS
    # ========================================================================

    def batch_get_requests(self, endpoints: List[str]) -> List[Optional[requests.Response]]:
        """
        Execute multiple GET requests in sequence

        Args:
            endpoints: List of endpoint paths

        Returns:
            List of response objects (None for failed requests)

        Example:
            responses = self.batch_get_requests(["/users/1", "/users/2", "/users/3"])
        """
        responses = []
        for i, endpoint in enumerate(endpoints, 1):
            try:
                self.logger.info(f"Batch GET {i}/{len(endpoints)}: {endpoint}")
                response = self.get_request(endpoint)
                responses.append(response)
            except Exception as e:
                self.logger.error(f"Batch GET failed for {endpoint}: {e}")
                responses.append(None)

        self.logger.info(f"Completed {len(responses)} batch GET requests")
        return responses

    def batch_post_requests(self, endpoint: str, payloads: List[Dict]) -> List[Optional[requests.Response]]:
        """
        Execute multiple POST requests to same endpoint

        Args:
            endpoint: API endpoint path
            payloads: List of payload dictionaries

        Returns:
            List of response objects (None for failed requests)

        Example:
            payloads = [{"name": "User1"}, {"name": "User2"}]
            responses = self.batch_post_requests("/users", payloads)
        """
        responses = []
        for i, payload in enumerate(payloads, 1):
            try:
                self.logger.info(f"Batch POST {i}/{len(payloads)}")
                response = self.post_request(endpoint, payload)
                responses.append(response)
            except Exception as e:
                self.logger.error(f"Batch POST failed for payload {i}: {e}")
                responses.append(None)

        self.logger.info(f"Completed {len(responses)} batch POST requests")
        return responses

    # ========================================================================
    # DATA FILTERING AND SORTING
    # ========================================================================

    def filter_response_data(self, response_data: List[Dict],
                             filter_key: str, filter_value: Any) -> List[Dict]:
        """
        Filter list of dictionaries by key-value pair

        Args:
            response_data: List of dictionaries to filter
            filter_key: Key to filter on
            filter_value: Value to match

        Returns:
            Filtered list of dictionaries

        Example:
            active_users = self.filter_response_data(users, "status", "active")
        """
        try:
            filtered = [item for item in response_data if item.get(filter_key) == filter_value]
            self.logger.info(f"Filtered {len(filtered)} items where {filter_key}={filter_value}")
            return filtered
        except Exception as e:
            self.logger.error(f"Failed to filter response data: {e}")
            raise

    def sort_response_data(self, response_data: List[Dict],
                           sort_key: str, reverse: bool = False) -> List[Dict]:
        """
        Sort list of dictionaries by key

        Args:
            response_data: List of dictionaries to sort
            sort_key: Key to sort by
            reverse: Sort in descending order if True

        Returns:
            Sorted list of dictionaries

        Example:
            sorted_users = self.sort_response_data(users, "created_at", reverse=True)
        """
        try:
            sorted_data = sorted(response_data, key=lambda x: x.get(sort_key, ""), reverse=reverse)
            self.logger.info(f"Sorted data by {sort_key} (reverse={reverse})")
            return sorted_data
        except Exception as e:
            self.logger.error(f"Failed to sort response data: {e}")
            raise

    # ========================================================================
    # PERFORMANCE TESTING METHODS
    # ========================================================================

    def measure_response_time(self, endpoint: str, method: str = "GET",
                              payload: Dict = None, iterations: int = 10) -> Dict[str, float]:
        """
        Measure response time statistics over multiple iterations

        Args:
            endpoint: API endpoint path
            method: HTTP method (GET, POST, etc.)
            payload: Request payload for POST/PUT/PATCH
            iterations: Number of iterations to run

        Returns:
            Dictionary with min, max, mean, median, and stdev statistics

        Example:
            stats = self.measure_response_time("/users", method="GET", iterations=10)
            print(f"Average response time: {stats['mean']:.3f}s")
        """
        response_times = []

        self.logger.info(f"Starting performance test: {iterations} iterations")

        for i in range(1, iterations + 1):
            try:
                if method.upper() == "GET":
                    response = self.get_request(endpoint)
                elif method.upper() == "POST":
                    response = self.post_request(endpoint, payload or {})
                elif method.upper() == "PUT":
                    response = self.put_request(endpoint, payload or {})
                elif method.upper() == "PATCH":
                    response = self.patch_request(endpoint, payload or {})
                else:
                    raise ValueError(f"Unsupported method: {method}")

                response_times.append(response.elapsed.total_seconds())
                self.logger.debug(f"Iteration {i}: {response.elapsed.total_seconds():.3f}s")

            except Exception as e:
                self.logger.warning(f"Iteration {i} failed: {e}")

        if response_times:
            stats = {
                'min': min(response_times),
                'max': max(response_times),
                'mean': statistics.mean(response_times),
                'median': statistics.median(response_times),
                'stdev': statistics.stdev(response_times) if len(response_times) > 1 else 0,
                'iterations': len(response_times)
            }

            self.logger.info(f"Performance test results: Min={stats['min']:.3f}s, "
                             f"Max={stats['max']:.3f}s, Mean={stats['mean']:.3f}s")

            # Attach to Allure
            allure.attach(
                json.dumps(stats, indent=2),
                name="Response Time Statistics",
                attachment_type=allure.attachment_type.JSON
            )

            return stats
        else:
            self.logger.error("No successful iterations completed")
            return {}

    def wait_for_api_response(self, endpoint: str, expected_status: int = 200,
                              max_attempts: int = 10, delay: int = 2) -> requests.Response:
        """
        Wait for API to return expected status code (polling mechanism)

        Args:
            endpoint: API endpoint path
            expected_status: Expected HTTP status code
            max_attempts: Maximum number of polling attempts
            delay: Delay between attempts in seconds

        Returns:
            Response object when expected status is received

        Raises:
            TimeoutError: If expected status not received after max_attempts

        Example:
            response = self.wait_for_api_response("/job/status", expected_status=200, max_attempts=30, delay=5)
        """
        for attempt in range(1, max_attempts + 1):
            try:
                self.logger.info(f"Polling attempt {attempt}/{max_attempts}")
                response = self.get_request(endpoint)

                if response.status_code == expected_status:
                    self.logger.info(f"[PASS] Got expected status {expected_status} on attempt {attempt}")
                    return response

                self.logger.warning(f"Got status {response.status_code}, expected {expected_status}")

            except Exception as e:
                self.logger.warning(f"Request failed: {e}")

            if attempt < max_attempts:
                self.logger.info(f"Waiting {delay} seconds before retry...")
                time.sleep(delay)

        error_msg = f"API did not return status {expected_status} after {max_attempts} attempts"
        self.logger.error(error_msg)
        raise TimeoutError(error_msg)

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def compare_responses(self, response1: Dict, response2: Dict) -> Dict:
        """
        Compare two JSON responses and identify differences

        Args:
            response1: First response dictionary
            response2: Second response dictionary

        Returns:
            Dictionary containing differences

        Example:
            differences = self.compare_responses(old_data, new_data)
        """
        differences = {}

        # Check for keys only in response1
        keys_only_in_r1 = set(response1.keys()) - set(response2.keys())
        if keys_only_in_r1:
            differences['only_in_response1'] = list(keys_only_in_r1)

        # Check for keys only in response2
        keys_only_in_r2 = set(response2.keys()) - set(response1.keys())
        if keys_only_in_r2:
            differences['only_in_response2'] = list(keys_only_in_r2)

        # Check for different values
        common_keys = set(response1.keys()) & set(response2.keys())
        different_values = {}
        for key in common_keys:
            if response1[key] != response2[key]:
                different_values[key] = {
                    'response1': response1[key],
                    'response2': response2[key]
                }

        if different_values:
            differences['different_values'] = different_values

        self.logger.info(f"Found {len(differences)} difference categories between responses")
        return differences

    def get_response_size(self, response: requests.Response) -> int:
        """
        Get response size in bytes

        Args:
            response: Response object

        Returns:
            Size in bytes

        Example:
            size = self.get_response_size(response)
            print(f"Response size: {size} bytes ({size/1024:.2f} KB)")
        """
        size = len(response.content)
        self.logger.info(f"Response size: {size} bytes ({size / 1024:.2f} KB)")
        return size

    def is_json_response(self, response: requests.Response) -> bool:
        """
        Check if response is JSON format

        Args:
            response: Response object

        Returns:
            True if response is JSON, False otherwise

        Example:
            if self.is_json_response(response):
                data = response.json()
        """
        try:
            response.json()
            return True
        except:
            return False

    def print_response(self, response: requests.Response):
        """
        Print formatted response for debugging

        Args:
            response: Response object to print

        Example:
            self.print_response(response)
        """
        print("\n" + "=" * 80)
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {response.elapsed.total_seconds():.3f}s")
        print(f"URL: {response.url}")
        print(f"Method: {response.request.method}")
        print("\nHeaders:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
        print("\nBody:")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text[:1000])  # Print first 1000 chars if not JSON
        print("=" * 80 + "\n")

    def save_response_to_file(self, response: requests.Response, filename: str):
        """
        Save response to file

        Args:
            response: Response object
            filename: Output filename

        Example:
            self.save_response_to_file(response, "user_response.json")
        """
        try:
            from pathlib import Path

            output_dir = Path("test_data/api_responses")
            output_dir.mkdir(parents=True, exist_ok=True)

            filepath = output_dir / filename

            with open(filepath, 'w', encoding='utf-8') as f:
                try:
                    json.dump(response.json(), f, indent=2)
                except:
                    f.write(response.text)

            self.logger.info(f"Response saved to: {filepath}")
        except Exception as e:
            self.logger.error(f"Failed to save response: {e}")

    def load_payload_from_file(self, filepath: str) -> Dict:
        """
        Load request payload from JSON file

        Args:
            filepath: Path to JSON file

        Returns:
            Payload as dictionary

        Example:
            payload = self.load_payload_from_file("test_data/json/payloads/create_user.json")
            response = self.post_request("/users", payload=payload)
        """
        try:
            return self.json_utility.read_json_file(filepath)
        except Exception as e:
            self.logger.error(f"Failed to load payload from file: {e}")
            raise

    # ========================================================================
    # LOGGING AND REPORTING METHODS
    # ========================================================================

    def _log_response(self, response: requests.Response):
        """
        Log response details

        Args:
            response: Response object to log
        """
        self.logger.info(f"Response Status: {response.status_code}")
        self.logger.info(f"Response Time: {response.elapsed.total_seconds():.3f}s")
        self.logger.debug(f"Response URL: {response.url}")
        self.logger.debug(f"Response Headers: {dict(response.headers)}")

        try:
            response_body = response.json()
            self.logger.debug(f"Response Body: {json.dumps(response_body, indent=2)[:500]}")
        except:
            self.logger.debug(f"Response Body: {response.text[:500]}")

    def _attach_request_to_allure(self, payload: Dict):
        """
        Attach request payload to Allure report

        Args:
            payload: Request payload dictionary
        """
        if payload:
            try:
                allure.attach(
                    self.json_utility.convert_to_json_string(payload, indent=2),
                    name="Request Payload",
                    attachment_type=allure.attachment_type.JSON
                )
            except Exception as e:
                self.logger.warning(f"Could not attach request to Allure: {e}")

    def _attach_response_to_allure(self, response: requests.Response):
        """
        Attach response to Allure report

        Args:
            response: Response object
        """
        try:
            # Attach response body
            try:
                response_json = response.json()
                allure.attach(
                    self.json_utility.convert_to_json_string(response_json, indent=2),
                    name=f"Response Body (Status: {response.status_code})",
                    attachment_type=allure.attachment_type.JSON
                )
            except:
                allure.attach(
                    response.text,
                    name=f"Response Body (Status: {response.status_code})",
                    attachment_type=allure.attachment_type.TEXT
                )

            # Attach response headers
            allure.attach(
                json.dumps(dict(response.headers), indent=2),
                name="Response Headers",
                attachment_type=allure.attachment_type.JSON
            )

            # Attach response metadata
            metadata = {
                "status_code": response.status_code,
                "response_time": f"{response.elapsed.total_seconds():.3f}s",
                "url": response.url,
                "method": response.request.method,
                "size": f"{len(response.content)} bytes"
            }
            allure.attach(
                json.dumps(metadata, indent=2),
                name="Response Metadata",
                attachment_type=allure.attachment_type.JSON
            )

        except Exception as e:
            self.logger.warning(f"Could not attach response to Allure: {e}")

    # ========================================================================
    # ASSERTION HELPERS
    # ========================================================================

    def assert_status_code(self, response: requests.Response, expected_status: int):
        """
        Assert status code with detailed logging

        Args:
            response: Response object
            expected_status: Expected status code

        Raises:
            AssertionError: If status code doesn't match
        """
        try:
            assert response.status_code == expected_status, \
                f"Expected status {expected_status}, got {response.status_code}. Response: {response.text[:200]}"
            self.logger.info(f"[PASS] Status code assertion passed: {response.status_code}")
        except AssertionError as e:
            self.logger.error(f"[FAIL] Status code assertion failed: {e}")
            self._attach_response_to_allure(response)
            raise

    def assert_response_contains_key(self, response_data: Dict, key: str):
        """
        Assert response contains key

        Args:
            response_data: Response JSON data
            key: Key to check

        Raises:
            AssertionError: If key not found
        """
        try:
            assert key in response_data, f"Key '{key}' not found in response. Available keys: {list(response_data.keys())}"
            self.logger.info(f"[PASS] Response contains key: {key}")
        except AssertionError as e:
            self.logger.error(f"[FAIL] Key assertion failed: {e}")
            raise

    def assert_response_value(self, response_data: Dict, key: str, expected_value: Any):
        """
        Assert response value for specific key

        Args:
            response_data: Response JSON data
            key: Key to check
            expected_value: Expected value

        Raises:
            AssertionError: If value doesn't match
        """
        try:
            actual_value = response_data.get(key)
            assert actual_value == expected_value, \
                f"Expected {key}='{expected_value}', got '{actual_value}'"
            self.logger.info(f"[PASS] Value assertion passed: {key}={expected_value}")
        except AssertionError as e:
            self.logger.error(f"[FAIL] Value assertion failed: {e}")
            raise

    def assert_response_not_empty(self, response_data: Any):
        """
        Assert response is not empty

        Args:
            response_data: Response data

        Raises:
            AssertionError: If response is empty
        """
        try:
            assert response_data, "Response is empty"
            self.logger.info("[PASS] Response is not empty")
        except AssertionError as e:
            self.logger.error(f"[FAIL] Empty response assertion failed: {e}")
            raise

    def assert_response_contains_text(self, response: requests.Response, text: str):
        """
        Assert response text contains specific string

        Args:
            response: Response object
            text: Text to search for

        Raises:
            AssertionError: If text not found
        """
        try:
            assert text in response.text, f"Text '{text}' not found in response"
            self.logger.info(f"[PASS] Response contains text: '{text}'")
        except AssertionError as e:
            self.logger.error(f"[FAIL] Text assertion failed: {e}")
            raise

    def assert_response_time_less_than(self, response: requests.Response, max_seconds: float):
        """
        Assert response time is less than specified seconds

        Args:
            response: Response object
            max_seconds: Maximum acceptable response time

        Raises:
            AssertionError: If response time exceeds max_seconds
        """
        try:
            actual_time = response.elapsed.total_seconds()
            assert actual_time < max_seconds, \
                f"Response time {actual_time:.3f}s exceeds maximum {max_seconds}s"
            self.logger.info(f"[PASS] Response time assertion passed: {actual_time:.3f}s < {max_seconds}s")
        except AssertionError as e:
            self.logger.error(f"[FAIL] Response time assertion failed: {e}")
            raise

    # ========================================================================
    # ADVANCED FEATURES
    # ========================================================================

    def retry_request_on_failure(self, method: str, endpoint: str,
                                 max_retries: int = 3, delay: int = 2,
                                 **kwargs) -> requests.Response:
        """
        Retry request on failure with exponential backoff

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            max_retries: Maximum number of retries
            delay: Initial delay between retries
            **kwargs: Additional arguments for the request

        Returns:
            Response object

        Raises:
            Exception: If all retries fail

        Example:
            response = self.retry_request_on_failure("GET", "/users/1", max_retries=3)
        """
        for attempt in range(1, max_retries + 1):
            try:
                self.logger.info(f"Request attempt {attempt}/{max_retries}")

                if method.upper() == "GET":
                    response = self.get_request(endpoint, **kwargs)
                elif method.upper() == "POST":
                    response = self.post_request(endpoint, **kwargs)
                elif method.upper() == "PUT":
                    response = self.put_request(endpoint, **kwargs)
                elif method.upper() == "DELETE":
                    response = self.delete_request(endpoint, **kwargs)
                else:
                    raise ValueError(f"Unsupported method: {method}")

                # Check if response is successful
                if 200 <= response.status_code < 300:
                    self.logger.info(f"[PASS] Request succeeded on attempt {attempt}")
                    return response
                else:
                    self.logger.warning(f"Request returned status {response.status_code}")

            except Exception as e:
                self.logger.warning(f"Attempt {attempt} failed: {e}")

            # Wait before retry (exponential backoff)
            if attempt < max_retries:
                wait_time = delay * (2 ** (attempt - 1))
                self.logger.info(f"Waiting {wait_time}s before retry...")
                time.sleep(wait_time)

        error_msg = f"Request failed after {max_retries} attempts"
        self.logger.error(error_msg)
        raise Exception(error_msg)

    def paginate_results(self, endpoint: str, page_param: str = "page",
                         per_page_param: str = "per_page", per_page: int = 100) -> List[Dict]:
        """
        Fetch all results from paginated API

        Args:
            endpoint: API endpoint
            page_param: Query parameter name for page number
            per_page_param: Query parameter name for items per page
            per_page: Number of items per page

        Returns:
            List of all items from all pages

        Example:
            all_users = self.paginate_results("/users", page_param="page", per_page=50)
        """
        all_items = []
        page = 1

        while True:
            self.logger.info(f"Fetching page {page}")
            params = {page_param: page, per_page_param: per_page}

            response = self.get_request(endpoint, params=params)
            self.validate_status_code(response, 200)

            data = self.extract_json_response(response)

            # Handle different pagination response formats
            if isinstance(data, list):
                items = data
            elif isinstance(data, dict) and 'data' in data:
                items = data['data']
            elif isinstance(data, dict) and 'results' in data:
                items = data['results']
            else:
                items = []

            if not items:
                break

            all_items.extend(items)
            self.logger.info(f"Retrieved {len(items)} items from page {page}")

            # Check if there are more pages
            if len(items) < per_page:
                break

            page += 1

        self.logger.info(f"Total items retrieved: {len(all_items)}")
        return all_items

    def upload_file_multipart(self, endpoint: str, file_path: str,
                              field_name: str = "file",
                              additional_data: Dict = None) -> requests.Response:
        """
        Upload file using multipart/form-data

        Args:
            endpoint: API endpoint
            file_path: Path to file to upload
            field_name: Form field name for the file
            additional_data: Additional form data

        Returns:
            Response object

        Example:
            response = self.upload_file_multipart("/upload", "test.pdf", field_name="document")
        """
        try:
            with open(file_path, 'rb') as file:
                files = {field_name: file}
                data = additional_data or {}

                self.logger.info(f"Uploading file: {file_path}")
                response = self.api_client.post(endpoint, data=data, files=files)

                self._log_response(response)
                self._attach_response_to_allure(response)

                return response

        except Exception as e:
            self.logger.error(f"File upload failed: {e}")
            raise

    def download_file(self, endpoint: str, save_path: str, params: Dict = None):
        """
        Download file from API

        Args:
            endpoint: API endpoint
            save_path: Path where to save the file
            params: Query parameters

        Example:
            self.download_file("/files/report.pdf", "downloads/report.pdf")
        """
        try:
            from pathlib import Path

            self.logger.info(f"Downloading file from: {endpoint}")
            response = self.get_request(endpoint, params=params)
            self.validate_status_code(response, 200)

            # Create directory if needed
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)

            # Save file
            with open(save_path, 'wb') as f:
                f.write(response.content)

            self.logger.info(f"File downloaded successfully to: {save_path}")

        except Exception as e:
            self.logger.error(f"File download failed: {e}")
            raise

    def get_request_with_retry_on_status(self, endpoint: str,
                                         retry_statuses: List[int] = [429, 503],
                                         max_retries: int = 5,
                                         delay: int = 5) -> requests.Response:
        """
        GET request with retry on specific status codes (e.g., rate limiting)

        Args:
            endpoint: API endpoint
            retry_statuses: List of status codes to retry on
            max_retries: Maximum number of retries
            delay: Delay between retries

        Returns:
            Response object

        Example:
            # Retry on 429 (Too Many Requests) and 503 (Service Unavailable)
            response = self.get_request_with_retry_on_status("/api/data", retry_statuses=[429, 503])
        """
        for attempt in range(1, max_retries + 1):
            response = self.get_request(endpoint)

            if response.status_code not in retry_statuses:
                return response

            self.logger.warning(f"Got status {response.status_code}, retrying... (Attempt {attempt}/{max_retries})")

            if attempt < max_retries:
                # Check for Retry-After header
                retry_after = response.headers.get('Retry-After')
                wait_time = int(retry_after) if retry_after else delay

                self.logger.info(f"Waiting {wait_time}s before retry...")
                time.sleep(wait_time)

        return response

    # ========================================================================
    # WEBHOOK AND ASYNC OPERATIONS
    # ========================================================================

    def trigger_webhook_and_wait(self, trigger_endpoint: str,
                                 status_endpoint: str,
                                 trigger_payload: Dict = None,
                                 max_wait: int = 60,
                                 poll_interval: int = 2) -> requests.Response:
        """
        Trigger webhook/async operation and wait for completion

        Args:
            trigger_endpoint: Endpoint to trigger the operation
            status_endpoint: Endpoint to check operation status
            trigger_payload: Payload for trigger request
            max_wait: Maximum time to wait in seconds
            poll_interval: Interval between status checks

        Returns:
            Final status response

        Example:
            response = self.trigger_webhook_and_wait(
                "/jobs/trigger",
                "/jobs/status/{job_id}",
                trigger_payload={"action": "process"}
            )
        """
        # Trigger the operation
        self.logger.info("Triggering async operation...")
        trigger_response = self.post_request(trigger_endpoint, payload=trigger_payload)
        self.validate_status_code(trigger_response, 202)

        # Extract job/operation ID
        job_id = self.extract_id_from_location_header(trigger_response)
        if not job_id:
            trigger_data = self.extract_json_response(trigger_response)
            job_id = trigger_data.get('id') or trigger_data.get('job_id')

        # Format status endpoint with job ID
        status_url = status_endpoint.format(job_id=job_id)

        # Poll for completion
        start_time = time.time()
        while time.time() - start_time < max_wait:
            status_response = self.get_request(status_url)
            status_data = self.extract_json_response(status_response)

            status = status_data.get('status', '').lower()

            if status in ['completed', 'success', 'done']:
                self.logger.info(f"[PASS] Operation completed successfully")
                return status_response
            elif status in ['failed', 'error']:
                error_msg = status_data.get('error', 'Operation failed')
                self.logger.error(f"[FAIL] Operation failed: {error_msg}")
                raise Exception(f"Async operation failed: {error_msg}")

            self.logger.info(f"Status: {status}, waiting...")
            time.sleep(poll_interval)

        raise TimeoutError(f"Operation did not complete within {max_wait} seconds")

# ============================================================================
# END OF BASE API SERVICE CLASS
# ============================================================================