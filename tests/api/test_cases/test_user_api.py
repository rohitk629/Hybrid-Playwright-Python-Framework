"""
User API Test Cases
"""
import pytest
import allure
from core.base.base_test import BaseTest
from tests.api.services.user_service import UserService
from core.utils.json_utility import JSONUtility
from faker import Faker


@allure.feature("User API")
@allure.story("User CRUD Operations")
class TestUserAPI(BaseTest):
    """User API test cases"""

    @pytest.fixture(autouse=True)
    def setup_api_test(self, setup_test):
        """Setup for API tests - depends on setup_test"""
        self.setup_api_client()
        self.user_service = UserService(self.api_client)
        self.json_utility = JSONUtility()
        self.faker = Faker()
        yield
        # Teardown if needed

    @allure.title("Test create user")
    @allure.description("Verify user can be created via API")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_create_user(self):
        """Test create user"""
        self.log_test_step("Step 1: Prepare user data")
        user_data = {
            "username": self.faker.user_name(),
            "email": self.faker.email(),
            "first_name": self.faker.first_name(),
            "last_name": self.faker.last_name(),
            "phone": self.faker.phone_number()
        }

        self.log_test_step("Step 2: Create user via API")
        user = self.user_service.create_user(user_data)

        self.log_test_step("Step 3: Validate user was created")
        self.assert_equals(user.username, user_data["username"], "Username should match")
        self.assert_equals(user.email, user_data["email"], "Email should match")
        self.assert_true(user.id is not None, "User ID should be assigned")

    @allure.title("Test get user by ID")
    @allure.description("Verify user can be retrieved by ID")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_get_user_by_id(self):
        """Test get user by ID"""
        # First create a user
        user_data = {
            "username": self.faker.user_name(),
            "email": self.faker.email(),
            "first_name": self.faker.first_name(),
            "last_name": self.faker.last_name()
        }
        created_user = self.user_service.create_user(user_data)

        self.log_test_step(f"Step 1: Get user by ID: {created_user.id}")
        retrieved_user = self.user_service.get_user_by_id(created_user.id)

        self.log_test_step("Step 2: Validate user data")
        self.assert_equals(retrieved_user.id, created_user.id, "User ID should match")
        self.assert_equals(retrieved_user.username, created_user.username,
                           "Username should match")

    @allure.title("Test JSON schema validation")
    @allure.description("Verify API response matches JSON schema")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_user_json_schema_validation(self):
        """Test JSON schema validation"""
        self.log_test_step("Step 1: Get user data")
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User"
        }
        user = self.user_service.create_user(user_data)

        self.log_test_step("Step 2: Validate JSON schema")
        schema_file = "core/models/schemas/user_schema.json"
        user_dict = user.model_dump()
        self.user_service.validate_json_schema(user_dict, schema_file)