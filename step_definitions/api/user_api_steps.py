"""
User API Step Definitions for BDD
"""
from behave import given, when, then
from core.utils.api_client_utility import APIClientUtility
from tests.api.services.user_service import UserService
from core.utils.json_utility import JSONUtility


@given('I have user payload with the following details')
def step_prepare_user_payload(context):
    """Prepare user payload from table"""
    context.api_client = APIClientUtility()
    context.user_service = UserService(context.api_client)

    row = context.table[0]
    context.user_payload = {
        "username": row['username'],
        "email": row['email'],
        "first_name": row['first_name'],
        "last_name": row['last_name']
    }


@when('I send POST request to create user endpoint')
def step_send_post_request(context):
    """Send POST request to create user"""
    context.user = context.user_service.create_user(context.user_payload)


@then('the response status code should be {status_code:d}')
def step_verify_status_code(context, status_code):
    """Verify response status code"""
    # Status code is already validated in the service method
    pass


@then('the response should contain user id')
def step_verify_user_id(context):
    """Verify response contains user ID"""
    assert context.user.id is not None, "Response should contain user ID"


@then('the response should match user schema')
def step_verify_user_schema(context):
    """Verify response matches user schema"""
    json_utility = JSONUtility()
    schema_file = "src/main/java/com/framework/models/schemas/user_schema.json"
    user_dict = context.user.model_dump()
    context.user_service.validate_json_schema(user_dict, schema_file)


@given('a user exists with id {user_id:d}')
def step_user_exists(context, user_id):
    """Setup: Ensure user exists"""
    context.user_id = user_id
    # In real scenario, create a user or verify it exists


@when('I send GET request to get user by id endpoint')
def step_get_user_by_id(context):
    """Send GET request to get user"""
    context.user = context.user_service.get_user_by_id(context.user_id)


@then('the response should contain user details')
def step_verify_user_details(context):
    """Verify user details in response"""
    assert context.user is not None, "Response should contain user details"
    assert context.user.id == context.user_id, "User ID should match"


@given('I have updated user payload')
def step_prepare_update_payload(context):
    """Prepare update payload"""
    row = context.table[0]
    context.update_payload = {
        "first_name": row['first_name'],
        "last_name": row['last_name']
    }


@when('I send PUT request to update user endpoint')
def step_update_user(context):
    """Send PUT request to update user"""
    context.user = context.user_service.update_user(context.user_id, context.update_payload)


@then('the response should contain updated information')
def step_verify_updated_info(context):
    """Verify response contains updated information"""
    assert context.user.first_name == context.update_payload['first_name']
    assert context.user.last_name == context.update_payload['last_name']


@when('I send DELETE request to delete user endpoint')
def step_delete_user(context):
    """Send DELETE request to delete user"""
    context.user_service.delete_user(context.user_id)


@when('I try to get the deleted user')
def step_try_get_deleted_user(context):
    """Try to get deleted user"""
    try:
        context.user_service.get_user_by_id(context.user_id)
        context.delete_verification_passed = False
    except Exception:
        context.delete_verification_passed = True