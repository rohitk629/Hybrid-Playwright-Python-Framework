"""
User API Service
"""
from core.base.base_api import BaseAPIService
from core.constants.api_endpoints import APIEndpoints
from core.models.pojo.user_pojo import UserPOJO
from typing import Dict, List
import allure


class UserService(BaseAPIService):
    """User API service"""

    @allure.step("Create user")
    def create_user(self, user_data: Dict) -> UserPOJO:
        """Create a new user"""
        response = self.post_request(APIEndpoints.USER_CREATE, payload=user_data)
        self.validate_status_code(response, 201)

        response_data = self.extract_json_response(response)
        return UserPOJO(**response_data)

    @allure.step("Get user by ID: {user_id}")
    def get_user_by_id(self, user_id: int) -> UserPOJO:
        """Get user by ID"""
        endpoint = APIEndpoints.USER_GET_BY_ID.format(user_id=user_id)
        response = self.get_request(endpoint)
        self.validate_status_code(response, 200)

        response_data = self.extract_json_response(response)
        return UserPOJO(**response_data)

    @allure.step("Update user: {user_id}")
    def update_user(self, user_id: int, user_data: Dict) -> UserPOJO:
        """Update user"""
        endpoint = APIEndpoints.USER_UPDATE.format(user_id=user_id)
        response = self.put_request(endpoint, payload=user_data)
        self.validate_status_code(response, 200)

        response_data = self.extract_json_response(response)
        return UserPOJO(**response_data)

    @allure.step("Delete user: {user_id}")
    def delete_user(self, user_id: int):
        """Delete user"""
        endpoint = APIEndpoints.USER_DELETE.format(user_id=user_id)
        response = self.delete_request(endpoint)
        self.validate_status_code(response, 204)

    @allure.step("Get all users")
    def get_all_users(self) -> List[UserPOJO]:
        """Get all users"""
        response = self.get_request(APIEndpoints.USER_LIST)
        self.validate_status_code(response, 200)

        response_data = self.extract_json_response(response)
        return [UserPOJO(**user) for user in response_data]

    @allure.step("Search users with query: {search_query}")
    def search_users(self, search_query: str) -> List[UserPOJO]:
        """Search users"""
        params = {"q": search_query}
        response = self.get_request(APIEndpoints.USER_SEARCH, params=params)
        self.validate_status_code(response, 200)

        response_data = self.extract_json_response(response)
        return [UserPOJO(**user) for user in response_data]