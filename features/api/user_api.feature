Feature: User API Operations
  As an API consumer
  I want to perform CRUD operations on users
  So that I can manage user data

  @smoke @api
  Scenario: Create a new user
    Given I have user payload with the following details:
      | username    | email              | first_name | last_name |
      | johndoe     | john@example.com   | John       | Doe       |
    When I send POST request to create user endpoint
    Then the response status code should be 201
    And the response should contain user id
    And the response should match user schema

  @regression @api
  Scenario: Get user by ID
    Given a user exists with id 1
    When I send GET request to get user by id endpoint
    Then the response status code should be 200
    And the response should contain user details
    And the response should match user schema

  @regression @api
  Scenario: Update user information
    Given a user exists with id 1
    And I have updated user payload:
      | first_name | last_name |
      | Jane       | Smith     |
    When I send PUT request to update user endpoint
    Then the response status code should be 200
    And the response should contain updated information

  @regression @api
  Scenario: Delete user
    Given a user exists with id 1
    When I send DELETE request to delete user endpoint
    Then the response status code should be 204
    When I try to get the deleted user
    Then the response status code should be 404