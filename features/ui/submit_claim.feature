Feature: Submit Insurance Claim
  As an authenticated user
  I want to submit insurance claims
  So that I can get reimbursement for medical expenses

  # Background runs before EVERY scenario in this feature
  Background: User is logged in
    Given I am logged in as a valid user
    And I navigate to "submit claim" page

  @smoke @ui @claims
  Scenario: Submit a valid medical claim
    When I fill in claim details:
      | field              | value           |
      | claim_type         | Medical         |
      | provider_name      | Dr. John Smith  |
      | service_date       | 2025-10-01      |
      | claim_amount       | 500.00          |
      | description        | Annual checkup  |
    And I attach supporting document "receipt.pdf"
    And I click the "Submit Claim" button
    Then I should see a success message "Claim submitted successfully"
    And the claim should appear in "Pending Claims" list
    And I should receive a claim reference number

  @regression @ui @claims
  Scenario: Submit claim without required documents
    When I fill in claim details:
      | field              | value           |
      | claim_type         | Dental          |
      | provider_name      | Dr. Jane Doe    |
      | service_date       | 2025-10-05      |
      | claim_amount       | 300.00          |
    And I click the "Submit Claim" button
    Then I should see an error message "Supporting documents are required"
    And the claim should not be submitted

  @regression @ui @claims
  Scenario Outline: Submit claims with different types
    When I fill in claim details:
      | field              | value              |
      | claim_type         | <claim_type>       |
      | provider_name      | <provider>         |
      | service_date       | <service_date>     |
      | claim_amount       | <amount>           |
    And I attach supporting document "receipt.pdf"
    And I click the "Submit Claim" button
    Then I should see a success message "Claim submitted successfully"

    Examples:
      | claim_type | provider        | service_date | amount  |
      | Medical    | Dr. Smith       | 2025-10-01   | 500.00  |
      | Dental     | Dr. Jones       | 2025-10-02   | 300.00  |
      | Vision     | Dr. Williams    | 2025-10-03   | 150.00  |
      | Pharmacy   | CVS Pharmacy    | 2025-10-04   | 75.00   |

  @smoke @ui @claims
  Scenario: Cancel claim submission
    When I start filling claim details
    And I click the "Cancel" button
    Then I should see a confirmation dialog "Are you sure you want to cancel?"
    When I confirm cancellation
    Then I should be on the "claims" page
    And no claim should be submitted