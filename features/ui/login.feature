Feature: User Login
  As a user
  I want to login to the application
  So that I can access my account

  Background:
    Given I am on the login page

  @smoke @ui
  Scenario: Successful login with valid credentials
    When I enter username "testuser@example.com"
    And I enter password "Test@123"
    And I click the login button
    Then I should be logged in successfully
    And I should see the dashboard

  @regression @ui
  Scenario: Login with invalid credentials
    When I enter username "invalid@example.com"
    And I enter password "wrongpassword"
    And I click the login button
    Then I should see an error message "Invalid credentials"
    And I should remain on the login page

  @regression @ui
  Scenario Outline: Login with multiple credentials
    When I enter username "<username>"
    And I enter password "<password>"
    And I click the login button
    Then I should see "<result>"

    Examples:
      | username              | password      | result                |
      | testuser@example.com  | Test@123      | Login successful      |
      | invalid@example.com   | wrong         | Invalid credentials   |
      | user@example.com      | Short1        | Password too short    |
      |                       | Test@123      | Username is required  |