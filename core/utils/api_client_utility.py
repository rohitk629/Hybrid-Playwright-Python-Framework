"""
API Client Utility Module
Provides comprehensive REST API testing utilities
Supports all HTTP methods, authentication, validations, and common API operations
"""

import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from requests.exceptions import RequestException, Timeout, ConnectionError
import json
import logging
from typing import Dict, Any, Optional, List, Union, Tuple
from pathlib import Path
import time
from datetime import datetime
import jsonschema
from jsonschema import validate, ValidationError
import xml.etree.ElementTree as ET
import xmltodict
import urllib.parse
import base64
import hashlib
import hmac

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIClientUtility:
    """
    Utility class for API testing and automation
    Provides methods for making HTTP requests, validations, and common API operations
    """

    def __init__(self, base_url: str = None, timeout: int = 30):
        """
        Initialize API Client Utility

        Args:
            base_url: Base URL for API endpoints
            timeout: Default request timeout in seconds
        """
        if base_url is None:
            from core.constants.application_constants import ApplicationConstants
            base_url = ApplicationConstants.API_BASE_URL

        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.default_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.session.headers.update(self.default_headers)
        self.response = None
        self.request_log = []
        self.response_log = []

        logger.info(f"APIClientUtility initialized with base URL: {base_url}")

    # ==================== Core HTTP Methods ====================

    def get(self, endpoint: str, params: Dict = None, headers: Dict = None,
            timeout: int = None, **kwargs) -> requests.Response:
        """
        Send GET request

        Args:
            endpoint: API endpoint (appended to base_url if provided)
            params: Query parameters
            headers: Request headers
            timeout: Request timeout
            **kwargs: Additional arguments for requests

        Returns:
            Response object
        """
        try:
            url = self._build_url(endpoint)
            timeout_val = timeout if timeout else self.timeout
            headers = self._merge_headers(headers)

            logger.info(f"GET request to: {url}")
            logger.info(f"Parameters: {params}")

            self.response = self.session.get(
                url,
                params=params,
                headers=headers,
                timeout=timeout_val,
                **kwargs
            )

            self._log_request('GET', url, params=params, headers=headers)
            self._log_response(self.response)

            logger.info(f"Response Status: {self.response.status_code}")
            return self.response

        except Exception as e:
            logger.error(f"Error in GET request: {str(e)}")
            raise

    def post(self, endpoint: str, data: Any = None, json_data: Dict = None,
             headers: Dict = None, timeout: int = None, **kwargs) -> requests.Response:
        """
        Send POST request

        Args:
            endpoint: API endpoint
            data: Request body (form data or raw)
            json_data: JSON request body
            headers: Request headers
            timeout: Request timeout
            **kwargs: Additional arguments

        Returns:
            Response object
        """
        try:
            url = self._build_url(endpoint)
            timeout_val = timeout if timeout else self.timeout
            headers = self._merge_headers(headers)

            logger.info(f"POST request to: {url}")
            logger.info(f"JSON Data: {json_data}")

            self.response = self.session.post(
                url,
                data=data,
                json=json_data,
                headers=headers,
                timeout=timeout_val,
                **kwargs
            )

            self._log_request('POST', url, data=data, json_data=json_data, headers=headers)
            self._log_response(self.response)

            logger.info(f"Response Status: {self.response.status_code}")
            return self.response

        except Exception as e:
            logger.error(f"Error in POST request: {str(e)}")
            raise

    def put(self, endpoint: str, data: Any = None, json_data: Dict = None,
            headers: Dict = None, timeout: int = None, **kwargs) -> requests.Response:
        """
        Send PUT request

        Args:
            endpoint: API endpoint
            data: Request body
            json_data: JSON request body
            headers: Request headers
            timeout: Request timeout
            **kwargs: Additional arguments

        Returns:
            Response object
        """
        try:
            url = self._build_url(endpoint)
            timeout_val = timeout if timeout else self.timeout
            headers = self._merge_headers(headers)

            logger.info(f"PUT request to: {url}")
            logger.info(f"JSON Data: {json_data}")

            self.response = self.session.put(
                url,
                data=data,
                json=json_data,
                headers=headers,
                timeout=timeout_val,
                **kwargs
            )

            self._log_request('PUT', url, data=data, json_data=json_data, headers=headers)
            self._log_response(self.response)

            logger.info(f"Response Status: {self.response.status_code}")
            return self.response

        except Exception as e:
            logger.error(f"Error in PUT request: {str(e)}")
            raise

    def patch(self, endpoint: str, data: Any = None, json_data: Dict = None,
              headers: Dict = None, timeout: int = None, **kwargs) -> requests.Response:
        """
        Send PATCH request

        Args:
            endpoint: API endpoint
            data: Request body
            json_data: JSON request body
            headers: Request headers
            timeout: Request timeout
            **kwargs: Additional arguments

        Returns:
            Response object
        """
        try:
            url = self._build_url(endpoint)
            timeout_val = timeout if timeout else self.timeout
            headers = self._merge_headers(headers)

            logger.info(f"PATCH request to: {url}")
            logger.info(f"JSON Data: {json_data}")

            self.response = self.session.patch(
                url,
                data=data,
                json=json_data,
                headers=headers,
                timeout=timeout_val,
                **kwargs
            )

            self._log_request('PATCH', url, data=data, json_data=json_data, headers=headers)
            self._log_response(self.response)

            logger.info(f"Response Status: {self.response.status_code}")
            return self.response

        except Exception as e:
            logger.error(f"Error in PATCH request: {str(e)}")
            raise

    def delete(self, endpoint: str, params: Dict = None, headers: Dict = None,
               timeout: int = None, **kwargs) -> requests.Response:
        """
        Send DELETE request

        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Request headers
            timeout: Request timeout
            **kwargs: Additional arguments

        Returns:
            Response object
        """
        try:
            url = self._build_url(endpoint)
            timeout_val = timeout if timeout else self.timeout
            headers = self._merge_headers(headers)

            logger.info(f"DELETE request to: {url}")

            self.response = self.session.delete(
                url,
                params=params,
                headers=headers,
                timeout=timeout_val,
                **kwargs
            )

            self._log_request('DELETE', url, params=params, headers=headers)
            self._log_response(self.response)

            logger.info(f"Response Status: {self.response.status_code}")
            return self.response

        except Exception as e:
            logger.error(f"Error in DELETE request: {str(e)}")
            raise

    def head(self, endpoint: str, params: Dict = None, headers: Dict = None,
             timeout: int = None, **kwargs) -> requests.Response:
        """
        Send HEAD request

        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Request headers
            timeout: Request timeout
            **kwargs: Additional arguments

        Returns:
            Response object
        """
        try:
            url = self._build_url(endpoint)
            timeout_val = timeout if timeout else self.timeout
            headers = self._merge_headers(headers)

            logger.info(f"HEAD request to: {url}")

            self.response = self.session.head(
                url,
                params=params,
                headers=headers,
                timeout=timeout_val,
                **kwargs
            )

            self._log_request('HEAD', url, params=params, headers=headers)
            self._log_response(self.response)

            logger.info(f"Response Status: {self.response.status_code}")
            return self.response

        except Exception as e:
            logger.error(f"Error in HEAD request: {str(e)}")
            raise

    def options(self, endpoint: str, headers: Dict = None, timeout: int = None,
                **kwargs) -> requests.Response:
        """
        Send OPTIONS request

        Args:
            endpoint: API endpoint
            headers: Request headers
            timeout: Request timeout
            **kwargs: Additional arguments

        Returns:
            Response object
        """
        try:
            url = self._build_url(endpoint)
            timeout_val = timeout if timeout else self.timeout
            headers = self._merge_headers(headers)

            logger.info(f"OPTIONS request to: {url}")

            self.response = self.session.options(
                url,
                headers=headers,
                timeout=timeout_val,
                **kwargs
            )

            self._log_request('OPTIONS', url, headers=headers)
            self._log_response(self.response)

            logger.info(f"Response Status: {self.response.status_code}")
            return self.response

        except Exception as e:
            logger.error(f"Error in OPTIONS request: {str(e)}")
            raise

    # ==================== Authentication Methods ====================

    def set_authentication(self, auth_type: str, **kwargs):
        """
        Set authentication

        Args:
            auth_type: Type of auth ('basic', 'bearer', 'api_key')
            **kwargs: Authentication parameters
        """
        if auth_type.lower() == 'basic':
            username = kwargs.get('username')
            password = kwargs.get('password')
            self.set_basic_auth(username, password)
        elif auth_type.lower() == 'bearer':
            token = kwargs.get('token')
            self.set_bearer_token(token)
        elif auth_type.lower() == 'api_key':
            api_key = kwargs.get('api_key')
            key_name = kwargs.get('key_name', 'X-API-Key')
            self.set_api_key(api_key, key_name)

    def set_basic_auth(self, username: str, password: str) -> None:
        """
        Set HTTP Basic Authentication

        Args:
            username: Username
            password: Password
        """
        self.session.auth = HTTPBasicAuth(username, password)
        logger.info("Basic authentication set")

    def set_digest_auth(self, username: str, password: str) -> None:
        """
        Set HTTP Digest Authentication

        Args:
            username: Username
            password: Password
        """
        self.session.auth = HTTPDigestAuth(username, password)
        logger.info("Digest authentication set")

    def set_bearer_token(self, token: str) -> None:
        """
        Set Bearer token authentication

        Args:
            token: Bearer token
        """
        self.session.headers.update({'Authorization': f'Bearer {token}'})
        logger.info("Bearer token authentication set")

    def set_api_key(self, key: str, header_name: str = 'X-API-Key') -> None:
        """
        Set API key authentication

        Args:
            key: API key
            header_name: Header name for API key
        """
        self.session.headers.update({header_name: key})
        logger.info(f"API key authentication set with header: {header_name}")

    def set_oauth_token(self, token: str, token_type: str = 'Bearer') -> None:
        """
        Set OAuth token

        Args:
            token: OAuth token
            token_type: Token type (Bearer, MAC, etc.)
        """
        self.session.headers.update({'Authorization': f'{token_type} {token}'})
        logger.info(f"OAuth {token_type} token set")

    def clear_auth(self) -> None:
        """Clear all authentication"""
        self.session.auth = None
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']
        logger.info("Authentication cleared")

    # ==================== Header Management ====================

    def set_header(self, key: str, value: str) -> None:
        """
        Set custom header

        Args:
            key: Header key
            value: Header value
        """
        self.session.headers[key] = value
        logger.info(f"Header set: {key} = {value}")

    def set_headers(self, headers: Dict[str, str]) -> None:
        """
        Set multiple headers

        Args:
            headers: Dictionary of headers
        """
        self.session.headers.update(headers)
        logger.info(f"Headers updated: {headers}")

    def remove_header(self, key: str) -> None:
        """
        Remove header

        Args:
            key: Header key to remove
        """
        if key in self.session.headers:
            del self.session.headers[key]
            logger.info(f"Header removed: {key}")

    def get_headers(self) -> Dict[str, str]:
        """
        Get current headers

        Returns:
            Dictionary of current headers
        """
        return dict(self.session.headers)

    def set_content_type(self, content_type: str) -> None:
        """
        Set Content-Type header

        Args:
            content_type: Content type (e.g., 'application/json')
        """
        self.set_header('Content-Type', content_type)

    def set_accept(self, accept: str) -> None:
        """
        Set Accept header

        Args:
            accept: Accept type (e.g., 'application/json')
        """
        self.set_header('Accept', accept)

    # ==================== Response Parsing ====================

    def get_response_json(self, response: requests.Response = None) -> Dict[str, Any]:
        """
        Parse response as JSON

        Args:
            response: Response object (uses last response if None)

        Returns:
            Parsed JSON dictionary
        """
        try:
            resp = response if response else self.response
            json_data = resp.json()
            logger.info("Response parsed as JSON")
            return json_data
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error getting response JSON: {str(e)}")
            raise

    def get_response_text(self, response: requests.Response = None) -> str:
        """
        Get response as text

        Args:
            response: Response object (uses last response if None)

        Returns:
            Response text
        """
        try:
            resp = response if response else self.response
            return resp.text
        except Exception as e:
            logger.error(f"Error getting response text: {str(e)}")
            raise

    def get_response_content(self, response: requests.Response = None) -> bytes:
        """
        Get response as bytes

        Args:
            response: Response object (uses last response if None)

        Returns:
            Response content as bytes
        """
        try:
            resp = response if response else self.response
            return resp.content
        except Exception as e:
            logger.error(f"Error getting response content: {str(e)}")
            raise

    def get_response_xml(self, response: requests.Response = None) -> ET.Element:
        """
        Parse response as XML

        Args:
            response: Response object (uses last response if None)

        Returns:
            XML Element tree
        """
        try:
            resp = response if response else self.response
            xml_root = ET.fromstring(resp.content)
            logger.info("Response parsed as XML")
            return xml_root
        except ET.ParseError as e:
            logger.error(f"Error parsing XML: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error getting response XML: {str(e)}")
            raise

    def xml_to_dict(self, response: requests.Response = None) -> Dict:
        """
        Convert XML response to dictionary

        Args:
            response: Response object (uses last response if None)

        Returns:
            Dictionary representation of XML
        """
        try:
            resp = response if response else self.response
            xml_dict = xmltodict.parse(resp.content)
            logger.info("XML converted to dictionary")
            return xml_dict
        except Exception as e:
            logger.error(f"Error converting XML to dict: {str(e)}")
            raise

    def get_status_code(self, response: requests.Response = None) -> int:
        """
        Get response status code

        Args:
            response: Response object (uses last response if None)

        Returns:
            HTTP status code
        """
        resp = response if response else self.response
        return resp.status_code

    def get_response_headers(self, response: requests.Response = None) -> Dict:
        """
        Get response headers

        Args:
            response: Response object (uses last response if None)

        Returns:
            Response headers dictionary
        """
        resp = response if response else self.response
        return dict(resp.headers)

    def get_response_time(self, response: requests.Response = None) -> float:
        """
        Get response time in seconds

        Args:
            response: Response object (uses last response if None)

        Returns:
            Response time in seconds
        """
        resp = response if response else self.response
        return resp.elapsed.total_seconds()

    # ==================== Response Validations ====================

    def assert_status_code(self, expected_code: int,
                           response: requests.Response = None) -> bool:
        """
        Assert response status code

        Args:
            expected_code: Expected status code
            response: Response object (uses last response if None)

        Returns:
            True if assertion passes

        Raises:
            AssertionError if status code doesn't match
        """
        resp = response if response else self.response
        actual_code = resp.status_code

        assert actual_code == expected_code, \
            f"Status code assertion failed. Expected: {expected_code}, Got: {actual_code}"

        logger.info(f"Status code assertion passed: {expected_code}")
        return True

    def assert_response_time(self, max_time: float,
                             response: requests.Response = None) -> bool:
        """
        Assert response time is within limit

        Args:
            max_time: Maximum allowed response time in seconds
            response: Response object (uses last response if None)

        Returns:
            True if assertion passes

        Raises:
            AssertionError if response time exceeds limit
        """
        resp = response if response else self.response
        actual_time = resp.elapsed.total_seconds()

        assert actual_time <= max_time, \
            f"Response time assertion failed. Expected: <={max_time}s, Got: {actual_time}s"

        logger.info(f"Response time assertion passed: {actual_time}s <= {max_time}s")
        return True

    def assert_json_contains(self, key: str, value: Any = None,
                             response: requests.Response = None) -> bool:
        """
        Assert JSON response contains key (and optionally value)

        Args:
            key: JSON key to check
            value: Expected value (optional)
            response: Response object (uses last response if None)

        Returns:
            True if assertion passes

        Raises:
            AssertionError if key not found or value doesn't match
        """
        json_data = self.get_response_json(response)

        assert key in json_data, f"Key '{key}' not found in JSON response"

        if value is not None:
            actual_value = json_data[key]
            assert actual_value == value, \
                f"Value assertion failed for key '{key}'. Expected: {value}, Got: {actual_value}"

        logger.info(f"JSON contains assertion passed for key: {key}")
        return True

    def assert_json_schema(self, schema: Dict, response: requests.Response = None) -> bool:
        """
        Validate JSON response against schema

        Args:
            schema: JSON schema dictionary
            response: Response object (uses last response if None)

        Returns:
            True if validation passes

        Raises:
            ValidationError if schema validation fails
        """
        try:
            json_data = self.get_response_json(response)
            validate(instance=json_data, schema=schema)
            logger.info("JSON schema validation passed")
            return True
        except ValidationError as e:
            logger.error(f"JSON schema validation failed: {str(e)}")
            raise

    def assert_header_exists(self, header_name: str,
                             response: requests.Response = None) -> bool:
        """
        Assert response header exists

        Args:
            header_name: Header name to check
            response: Response object (uses last response if None)

        Returns:
            True if assertion passes

        Raises:
            AssertionError if header not found
        """
        resp = response if response else self.response
        headers = resp.headers

        assert header_name in headers, f"Header '{header_name}' not found in response"

        logger.info(f"Header exists assertion passed: {header_name}")
        return True

    def assert_header_value(self, header_name: str, expected_value: str,
                            response: requests.Response = None) -> bool:
        """
        Assert response header value

        Args:
            header_name: Header name
            expected_value: Expected header value
            response: Response object (uses last response if None)

        Returns:
            True if assertion passes

        Raises:
            AssertionError if header value doesn't match
        """
        resp = response if response else self.response
        actual_value = resp.headers.get(header_name)

        assert actual_value == expected_value, \
            f"Header value assertion failed for '{header_name}'. Expected: {expected_value}, Got: {actual_value}"

        logger.info(f"Header value assertion passed: {header_name}")
        return True

    def assert_content_type(self, expected_type: str,
                            response: requests.Response = None) -> bool:
        """
        Assert response Content-Type

        Args:
            expected_type: Expected content type
            response: Response object (uses last response if None)

        Returns:
            True if assertion passes
        """
        return self.assert_header_value('Content-Type', expected_type, response)

    # ==================== JSON Path Operations ====================

    def get_json_value(self, json_path: str, response: requests.Response = None) -> Any:
        """
        Get value from JSON response using dot notation path

        Args:
            json_path: Path in dot notation (e.g., 'data.user.name')
            response: Response object (uses last response if None)

        Returns:
            Value at the specified path
        """
        try:
            json_data = self.get_response_json(response)
            keys = json_path.split('.')
            value = json_data

            for key in keys:
                if '[' in key and ']' in key:
                    # Handle array index
                    key_name = key[:key.index('[')]
                    index = int(key[key.index('[') + 1:key.index(']')])
                    value = value[key_name][index]
                else:
                    value = value[key]

            logger.info(f"Got JSON value for path '{json_path}': {value}")
            return value

        except (KeyError, IndexError, TypeError) as e:
            logger.error(f"Error getting JSON value for path '{json_path}': {str(e)}")
            raise

    def assert_json_value(self, json_path: str, expected_value: Any,
                          response: requests.Response = None) -> bool:
        """
        Assert JSON value at path matches expected

        Args:
            json_path: Path in dot notation
            expected_value: Expected value
            response: Response object (uses last response if None)

        Returns:
            True if assertion passes
        """
        actual_value = self.get_json_value(json_path, response)

        assert actual_value == expected_value, \
            f"JSON value assertion failed for path '{json_path}'. Expected: {expected_value}, Got: {actual_value}"

        logger.info(f"JSON value assertion passed for path: {json_path}")
        return True

    # ==================== File Operations ====================

    def upload_file(self, endpoint: str, file_path: str, file_key: str = 'file',
                    additional_data: Dict = None, headers: Dict = None) -> requests.Response:
        """
        Upload file

        Args:
            endpoint: API endpoint
            file_path: Path to file
            file_key: Form field name for file
            additional_data: Additional form data
            headers: Request headers

        Returns:
            Response object
        """
        try:
            url = self._build_url(endpoint)

            with open(file_path, 'rb') as f:
                files = {file_key: f}
                data = additional_data if additional_data else {}

                logger.info(f"Uploading file: {file_path}")

                self.response = self.session.post(
                    url,
                    files=files,
                    data=data,
                    headers=headers,
                    timeout=self.timeout
                )

            logger.info(f"File upload response status: {self.response.status_code}")
            return self.response

        except Exception as e:
            logger.error(f"Error uploading file: {str(e)}")
            raise

    def download_file(self, endpoint: str, save_path: str, params: Dict = None,
                      headers: Dict = None) -> str:
        """
        Download file

        Args:
            endpoint: API endpoint
            save_path: Path to save downloaded file
            params: Query parameters
            headers: Request headers

        Returns:
            Path to downloaded file
        """
        try:
            url = self._build_url(endpoint)
            headers = self._merge_headers(headers)

            logger.info(f"Downloading file from: {url}")

            self.response = self.session.get(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout,
                stream=True
            )

            with open(save_path, 'wb') as f:
                for chunk in self.response.iter_content(chunk_size=8192):
                    f.write(chunk)

            logger.info(f"File downloaded to: {save_path}")
            return save_path

        except Exception as e:
            logger.error(f"Error downloading file: {str(e)}")
            raise

    # ==================== Cookie Operations ====================

    def get_cookies(self) -> Dict[str, str]:
        """
        Get all cookies

        Returns:
            Dictionary of cookies
        """
        return dict(self.session.cookies)

    def get_cookie(self, name: str) -> Optional[str]:
        """
        Get specific cookie value

        Args:
            name: Cookie name

        Returns:
            Cookie value or None
        """
        return self.session.cookies.get(name)

    def set_cookie(self, name: str, value: str, domain: str = None,
                   path: str = '/') -> None:
        """
        Set cookie

        Args:
            name: Cookie name
            value: Cookie value
            domain: Cookie domain
            path: Cookie path
        """
        cookie_dict = {'name': name, 'value': value, 'path': path}
        if domain:
            cookie_dict['domain'] = domain

        self.session.cookies.set(**cookie_dict)
        logger.info(f"Cookie set: {name}")

    def clear_cookies(self) -> None:
        """Clear all cookies"""
        self.session.cookies.clear()
        logger.info("All cookies cleared")

    # ==================== Utility Methods ====================

    def _build_url(self, endpoint: str) -> str:
        """
        Build full URL from base URL and endpoint

        Args:
            endpoint: API endpoint

        Returns:
            Full URL
        """
        if endpoint.startswith('http://') or endpoint.startswith('https://'):
            return endpoint

        if self.base_url:
            return urllib.parse.urljoin(self.base_url, endpoint.lstrip('/'))

        return endpoint

    def _merge_headers(self, headers: Dict = None) -> Dict:
        """
        Merge custom headers with session headers

        Args:
            headers: Custom headers

        Returns:
            Merged headers dictionary
        """
        if headers:
            merged = dict(self.session.headers)
            merged.update(headers)
            return merged
        return dict(self.session.headers)

    def _log_request(self, method: str, url: str, **kwargs) -> None:
        """Log request details"""
        request_info = {
            'timestamp': datetime.now().isoformat(),
            'method': method,
            'url': url,
            **kwargs
        }
        self.request_log.append(request_info)

    def _log_response(self, response: requests.Response) -> None:
        """Log response details"""
        response_info = {
            'timestamp': datetime.now().isoformat(),
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'response_time': response.elapsed.total_seconds()
        }
        self.response_log.append(response_info)

    def set_base_url(self, base_url: str) -> None:
        """
        Set or update base URL

        Args:
            base_url: Base URL for API
        """
        self.base_url = base_url
        logger.info(f"Base URL set to: {base_url}")

    def set_timeout(self, timeout: int) -> None:
        """
        Set default timeout

        Args:
            timeout: Timeout in seconds
        """
        self.timeout = timeout
        logger.info(f"Timeout set to: {timeout} seconds")

    def enable_ssl_verification(self, verify: bool = True) -> None:
        """
        Enable/disable SSL certificate verification

        Args:
            verify: True to enable, False to disable
        """
        self.session.verify = verify
        logger.info(f"SSL verification: {'enabled' if verify else 'disabled'}")

    def set_proxy(self, proxy_url: str, protocol: str = 'http') -> None:
        """
        Set proxy

        Args:
            proxy_url: Proxy URL
            protocol: Protocol ('http' or 'https')
        """
        self.session.proxies = {protocol: proxy_url}
        logger.info(f"Proxy set for {protocol}: {proxy_url}")

    def clear_proxy(self) -> None:
        """Clear proxy settings"""
        self.session.proxies = {}
        logger.info("Proxy settings cleared")

    def get_request_log(self) -> List[Dict]:
        """
        Get request log

        Returns:
            List of logged requests
        """
        return self.request_log

    def get_response_log(self) -> List[Dict]:
        """
        Get response log

        Returns:
            List of logged responses
        """
        return self.response_log

    def clear_logs(self) -> None:
        """Clear request and response logs"""
        self.request_log = []
        self.response_log = []
        logger.info("Request and response logs cleared")

    def save_response_to_file(self, file_path: str, response: requests.Response = None) -> None:
        """
        Save response to file

        Args:
            file_path: Path to save file
            response: Response object (uses last response if None)
        """
        try:
            resp = response if response else self.response

            with open(file_path, 'w', encoding='utf-8') as f:
                if resp.headers.get('Content-Type', '').startswith('application/json'):
                    json.dump(resp.json(), f, indent=4)
                else:
                    f.write(resp.text)

            logger.info(f"Response saved to: {file_path}")

        except Exception as e:
            logger.error(f"Error saving response to file: {str(e)}")
            raise

    def close_session(self) -> None:
        """Close session and cleanup"""
        self.session.close()
        logger.info("Session closed")

    # ==================== Advanced Operations ====================

    def retry_request(self, method: str, endpoint: str, max_retries: int = 3,
                      retry_delay: float = 1.0, **kwargs) -> requests.Response:
        """
        Retry request on failure

        Args:
            method: HTTP method
            endpoint: API endpoint
            max_retries: Maximum number of retries
            retry_delay: Delay between retries in seconds
            **kwargs: Request parameters

        Returns:
            Response object
        """
        method = method.upper()
        request_methods = {
            'GET': self.get,
            'POST': self.post,
            'PUT': self.put,
            'PATCH': self.patch,
            'DELETE': self.delete
        }

        if method not in request_methods:
            raise ValueError(f"Unsupported HTTP method: {method}")

        for attempt in range(max_retries):
            try:
                logger.info(f"Attempt {attempt + 1} of {max_retries}")
                response = request_methods[method](endpoint, **kwargs)

                if response.status_code < 500:  # Success or client error
                    return response

                logger.warning(f"Server error {response.status_code}, retrying...")

            except RequestException as e:
                logger.warning(f"Request failed: {str(e)}, retrying...")

            if attempt < max_retries - 1:
                time.sleep(retry_delay)

        raise Exception(f"Request failed after {max_retries} attempts")

    def batch_requests(self, requests_list: List[Dict]) -> List[requests.Response]:
        """
        Execute multiple requests in batch

        Args:
            requests_list: List of request dictionaries containing 'method', 'endpoint', and optional params

        Returns:
            List of Response objects
        """
        responses = []

        for req in requests_list:
            method = req.get('method', 'GET').upper()
            endpoint = req.get('endpoint')
            params = req.get('params', {})

            logger.info(f"Batch request: {method} {endpoint}")

            if method == 'GET':
                response = self.get(endpoint, **params)
            elif method == 'POST':
                response = self.post(endpoint, **params)
            elif method == 'PUT':
                response = self.put(endpoint, **params)
            elif method == 'PATCH':
                response = self.patch(endpoint, **params)
            elif method == 'DELETE':
                response = self.delete(endpoint, **params)
            else:
                logger.warning(f"Unsupported method in batch: {method}")
                continue

            responses.append(response)

        logger.info(f"Batch completed: {len(responses)} requests executed")
        return responses

    def parallel_requests(self, requests_list: List[Dict], max_workers: int = 5) -> List[requests.Response]:
        """
        Execute multiple requests in parallel

        Args:
            requests_list: List of request dictionaries
            max_workers: Maximum number of concurrent workers

        Returns:
            List of Response objects
        """
        from concurrent.futures import ThreadPoolExecutor, as_completed

        def execute_request(req):
            method = req.get('method', 'GET').upper()
            endpoint = req.get('endpoint')
            params = req.get('params', {})

            if method == 'GET':
                return self.get(endpoint, **params)
            elif method == 'POST':
                return self.post(endpoint, **params)
            elif method == 'PUT':
                return self.put(endpoint, **params)
            elif method == 'PATCH':
                return self.patch(endpoint, **params)
            elif method == 'DELETE':
                return self.delete(endpoint, **params)

        responses = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(execute_request, req): req for req in requests_list}

            for future in as_completed(futures):
                try:
                    response = future.result()
                    responses.append(response)
                except Exception as e:
                    logger.error(f"Parallel request failed: {str(e)}")

        logger.info(f"Parallel execution completed: {len(responses)} requests")
        return responses

    def wait_for_status(self, endpoint: str, expected_status: int,
                        timeout: int = 60, interval: int = 2) -> requests.Response:
        """
        Poll endpoint until expected status is received

        Args:
            endpoint: API endpoint
            expected_status: Expected status code
            timeout: Maximum wait time in seconds
            interval: Polling interval in seconds

        Returns:
            Response object with expected status
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                response = self.get(endpoint)

                if response.status_code == expected_status:
                    logger.info(f"Expected status {expected_status} received")
                    return response

                logger.info(f"Status {response.status_code}, waiting for {expected_status}...")
                time.sleep(interval)

            except Exception as e:
                logger.warning(f"Request failed: {str(e)}, retrying...")
                time.sleep(interval)

        raise TimeoutError(f"Expected status {expected_status} not received within {timeout} seconds")

    def wait_for_condition(self, endpoint: str, condition_func,
                           timeout: int = 60, interval: int = 2, **kwargs) -> requests.Response:
        """
        Poll endpoint until condition function returns True

        Args:
            endpoint: API endpoint
            condition_func: Function that takes response and returns bool
            timeout: Maximum wait time in seconds
            interval: Polling interval in seconds
            **kwargs: Additional request parameters

        Returns:
            Response object when condition is met
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                response = self.get(endpoint, **kwargs)

                if condition_func(response):
                    logger.info("Condition met")
                    return response

                logger.info("Condition not met, waiting...")
                time.sleep(interval)

            except Exception as e:
                logger.warning(f"Request failed: {str(e)}, retrying...")
                time.sleep(interval)

        raise TimeoutError(f"Condition not met within {timeout} seconds")

    # ==================== GraphQL Support ====================

    def graphql_query(self, endpoint: str, query: str, variables: Dict = None,
                      operation_name: str = None, headers: Dict = None) -> requests.Response:
        """
        Execute GraphQL query

        Args:
            endpoint: GraphQL endpoint
            query: GraphQL query string
            variables: Query variables
            operation_name: Operation name
            headers: Request headers

        Returns:
            Response object
        """
        payload = {'query': query}

        if variables:
            payload['variables'] = variables

        if operation_name:
            payload['operationName'] = operation_name

        logger.info(f"Executing GraphQL query: {operation_name or 'unnamed'}")

        return self.post(endpoint, json_data=payload, headers=headers)

    def graphql_mutation(self, endpoint: str, mutation: str, variables: Dict = None,
                         operation_name: str = None, headers: Dict = None) -> requests.Response:
        """
        Execute GraphQL mutation

        Args:
            endpoint: GraphQL endpoint
            mutation: GraphQL mutation string
            variables: Mutation variables
            operation_name: Operation name
            headers: Request headers

        Returns:
            Response object
        """
        payload = {'query': mutation}

        if variables:
            payload['variables'] = variables

        if operation_name:
            payload['operationName'] = operation_name

        logger.info(f"Executing GraphQL mutation: {operation_name or 'unnamed'}")

        return self.post(endpoint, json_data=payload, headers=headers)

    # ==================== SOAP Support ====================

    def soap_request(self, endpoint: str, soap_action: str, soap_body: str,
                     headers: Dict = None) -> requests.Response:
        """
        Send SOAP request

        Args:
            endpoint: SOAP endpoint
            soap_action: SOAP action header
            soap_body: SOAP envelope XML
            headers: Additional headers

        Returns:
            Response object
        """
        soap_headers = {
            'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': soap_action
        }

        if headers:
            soap_headers.update(headers)

        logger.info(f"Sending SOAP request with action: {soap_action}")

        return self.post(endpoint, data=soap_body, headers=soap_headers)

    # ==================== Performance Testing ====================

    def measure_response_time(self, method: str, endpoint: str,
                              iterations: int = 10, **kwargs) -> Dict[str, float]:
        """
        Measure response time statistics

        Args:
            method: HTTP method
            endpoint: API endpoint
            iterations: Number of iterations
            **kwargs: Request parameters

        Returns:
            Dictionary with min, max, avg response times
        """
        method = method.upper()
        request_methods = {
            'GET': self.get,
            'POST': self.post,
            'PUT': self.put,
            'PATCH': self.patch,
            'DELETE': self.delete
        }

        if method not in request_methods:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response_times = []

        logger.info(f"Measuring response time over {iterations} iterations")

        for i in range(iterations):
            start_time = time.time()
            response = request_methods[method](endpoint, **kwargs)
            end_time = time.time()

            response_times.append(end_time - start_time)
            logger.info(f"Iteration {i + 1}: {response_times[-1]:.3f}s")

        stats = {
            'min': min(response_times),
            'max': max(response_times),
            'avg': sum(response_times) / len(response_times),
            'total': sum(response_times),
            'iterations': iterations
        }

        logger.info(f"Performance stats - Min: {stats['min']:.3f}s, "
                    f"Max: {stats['max']:.3f}s, Avg: {stats['avg']:.3f}s")

        return stats

    def load_test(self, method: str, endpoint: str, duration: int = 60,
                  requests_per_second: int = 10, **kwargs) -> Dict[str, Any]:
        """
        Perform simple load test

        Args:
            method: HTTP method
            endpoint: API endpoint
            duration: Test duration in seconds
            requests_per_second: Target requests per second
            **kwargs: Request parameters

        Returns:
            Dictionary with test results
        """
        method = method.upper()
        request_methods = {
            'GET': self.get,
            'POST': self.post,
            'PUT': self.put,
            'PATCH': self.patch,
            'DELETE': self.delete
        }

        if method not in request_methods:
            raise ValueError(f"Unsupported HTTP method: {method}")

        start_time = time.time()
        interval = 1.0 / requests_per_second

        total_requests = 0
        successful_requests = 0
        failed_requests = 0
        response_times = []

        logger.info(f"Starting load test: {requests_per_second} req/s for {duration}s")

        while time.time() - start_time < duration:
            request_start = time.time()

            try:
                response = request_methods[method](endpoint, **kwargs)
                response_times.append(self.get_response_time(response))

                if 200 <= response.status_code < 300:
                    successful_requests += 1
                else:
                    failed_requests += 1

            except Exception as e:
                failed_requests += 1
                logger.warning(f"Request failed: {str(e)}")

            total_requests += 1

            # Sleep to maintain target rate
            elapsed = time.time() - request_start
            if elapsed < interval:
                time.sleep(interval - elapsed)

        actual_duration = time.time() - start_time

        results = {
            'duration': actual_duration,
            'total_requests': total_requests,
            'successful_requests': successful_requests,
            'failed_requests': failed_requests,
            'requests_per_second': total_requests / actual_duration,
            'success_rate': (successful_requests / total_requests * 100) if total_requests > 0 else 0,
            'avg_response_time': sum(response_times) / len(response_times) if response_times else 0,
            'min_response_time': min(response_times) if response_times else 0,
            'max_response_time': max(response_times) if response_times else 0
        }

        logger.info(f"Load test completed - Total: {total_requests}, "
                    f"Success: {successful_requests}, Failed: {failed_requests}")

        return results

    # ==================== Data Extraction ====================

    def extract_value_by_regex(self, pattern: str, response: requests.Response = None) -> Optional[str]:
        """
        Extract value from response using regex

        Args:
            pattern: Regex pattern
            response: Response object (uses last response if None)

        Returns:
            Matched value or None
        """
        import re

        try:
            resp = response if response else self.response
            text = resp.text

            match = re.search(pattern, text)
            if match:
                value = match.group(1) if match.groups() else match.group(0)
                logger.info(f"Extracted value by regex: {value}")
                return value

            logger.warning(f"No match found for pattern: {pattern}")
            return None

        except Exception as e:
            logger.error(f"Error extracting value by regex: {str(e)}")
            return None

    def extract_all_by_regex(self, pattern: str, response: requests.Response = None) -> List[str]:
        """
        Extract all matching values from response using regex

        Args:
            pattern: Regex pattern
            response: Response object (uses last response if None)

        Returns:
            List of matched values
        """
        import re

        try:
            resp = response if response else self.response
            text = resp.text

            matches = re.findall(pattern, text)
            logger.info(f"Extracted {len(matches)} values by regex")
            return matches

        except Exception as e:
            logger.error(f"Error extracting values by regex: {str(e)}")
            return []

    # ==================== Comparison Methods ====================

    def compare_responses(self, response1: requests.Response,
                          response2: requests.Response) -> Dict[str, Any]:
        """
        Compare two responses

        Args:
            response1: First response
            response2: Second response

        Returns:
            Dictionary with comparison results
        """
        comparison = {
            'status_codes_match': response1.status_code == response2.status_code,
            'status_code_1': response1.status_code,
            'status_code_2': response2.status_code,
            'response_times': {
                'response_1': response1.elapsed.total_seconds(),
                'response_2': response2.elapsed.total_seconds()
            }
        }

        try:
            json1 = response1.json()
            json2 = response2.json()
            comparison['json_match'] = json1 == json2
            comparison['json_1'] = json1
            comparison['json_2'] = json2
        except:
            comparison['json_match'] = response1.text == response2.text
            comparison['text_match'] = response1.text == response2.text

        logger.info("Response comparison completed")
        return comparison

    # ==================== Alias Methods for Base API Compatibility ====================

    def validate_response_status(self, response: requests.Response, expected_status: int):
        """
        Validate response status code (alias for assert_status_code)

        Args:
            response: Response object to validate
            expected_status: Expected HTTP status code

        Raises:
            AssertionError if status code doesn't match
        """
        return self.assert_status_code(expected_status, response)

    def validate_response_time(self, response: requests.Response, max_time: float):
        """
        Validate response time (alias for assert_response_time)

        Args:
            response: Response object to validate
            max_time: Maximum acceptable response time in seconds

        Raises:
            AssertionError if response time exceeds max_time
        """
        return self.assert_response_time(max_time, response)

    def validate_json_schema(self, response_data: Dict, schema: Dict):
        """
        Validate JSON response against schema (alias for assert_json_schema)

        Args:
            response_data: Response JSON data as dictionary
            schema: JSON schema dictionary

        Raises:
            ValidationError if schema validation fails
        """
        try:
            validate(instance=response_data, schema=schema)
            logger.info("JSON schema validation passed")
            return True
        except ValidationError as e:
            logger.error(f"JSON schema validation failed: {str(e)}")
            raise

    def extract_json_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Extract JSON from response (alias for get_response_json)

        Args:
            response: Response object

        Returns:
            JSON data as dictionary
        """
        return self.get_response_json(response)

