"""
Submit Claim Test Cases
Comprehensive test suite for claim submission functionality
"""

import pytest
import allure
from datetime import datetime, timedelta
from pathlib import Path
from core.base.base_test import BaseTest
from core.constants.error_messages import ErrorMessages
from tests.ui.pages.login_page import LoginPage
from tests.ui.pages.submit_claim_page import SubmitClaimPage
from faker import Faker


@allure.feature("Claims Management")
@allure.story("Submit Claim")
class TestSubmitClaim(BaseTest):
    """Submit claim test cases"""

    @pytest.fixture(autouse=True)
    def setup_claim_test(self, setup_test):
        """Setup for claim submission tests - depends on setup_test"""
        # Initialize instance variables
        self.setup_browser()
        self.faker = Faker()

        # Initialize page objects
        self.login_page = LoginPage(self.browser_utility)
        self.claim_page = SubmitClaimPage(self.browser_utility)

        # Navigate to login page
        login_url = "https://qos214.sk.bluecross.ca/IdPLogin/LoginMemberWeb"
        self.login_page.navigate_to(login_url)

        # Login with valid credentials
        self.login_page.login("jcastro@gmail.com", "SBCqatester2024!")
        self.login_page.wait_for_page_load(timeout=100000)

        # Navigate to submit claim page
        self.claim_page.navigate_to_submit_claim()
        self.claim_page.wait_for_form_load()

        yield
        # Additional teardown if needed

    def _generate_test_claim_data(self, claim_type="Dental"):
        """Generate test claim data with realistic values"""
        service_date = datetime.now() - timedelta(days=self.faker.random_int(min=1, max=30))

        return {
            "claim_type": claim_type,
            "patient_name": self.faker.name(),
            "policy_number": f"BC{self.faker.random_number(digits=8)}",
            "service_date": service_date.strftime("%m/%d/%Y"),
            "provider_name": f"Dr. {self.faker.last_name()} Medical Center",
            "claim_amount": f"{self.faker.random_int(min=50, max=5000)}",
            "description": f"Medical service: {self.faker.sentence()}"
        }

    @allure.title("Test successful error message when workplace or motor vehicle injury is selected")
    @allure.description("Verify the error message when workplace or motor vehicle injury is selected, and Next button is disabled")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_claim_details_screen_yes_injury(self):
        """Test successful claim submission"""
        self.log_test_step("Step 1: Generate test claim data")
        claim_data = self._generate_test_claim_data()

        self.log_test_step("Step 2: Select claim type as Dental")
        self.claim_page.select_claim_type("Dental")

        self.log_test_step("Step 3: Wait for Claim content Title to be visible")
        self.claim_page.wait_for_content_title(timeout=5000)

        self.log_test_step("Step 4: Verify the Claim content Title contains the word 'Dental'")
        self.assert_contains(self.claim_page.get_content_title().lower(), "dental",)

        self.log_test_step("Step 5: Select 'Yes' for workplace injury")
        self.claim_page.select_workplace_injury()

        self.log_test_step("Step 5: Verify the workplace injury or motor vehicle injury error message is displayed")
        self.assert_equals(self.claim_page.get_injury_error_message(), ErrorMessages.WORKPLACE_OR_MOTOR_VEHICLE_INJURY_ERROR_MESSAGE,
                          "Workplace or motor vehicle injury error message should be displayed")


    @allure.title("Test successful Dental claim Details Screen submission")
    @allure.description("Verify user can successfully submit a Dental claim with all required information")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_claim_details_screen_no_injury(self):
        """Test successful claim submission"""
        self.log_test_step("Step 1: Generate test claim data")
        claim_data = self._generate_test_claim_data()

        self.log_test_step("Step 2: Select claim type as Dental")
        self.claim_page.select_claim_type("Dental")

        self.log_test_step("Step 3: Wait for Claim content Title to be visible")
        self.claim_page.wait_for_content_title(timeout=5000)

        self.log_test_step("Step 4: Verify the Claim content Title contains the word 'Dental'")
        self.assert_contains(self.claim_page.get_content_title().lower(), "dental",)

    @allure.title("Test claim submission with missing required fields")
    @allure.description("Verify validation errors when required fields are missing")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_claim_submission_missing_required_fields(self):
        """Test claim submission with missing required fields"""
        self.log_test_step("Step 1: Click submit without filling any fields")
        self.claim_page.click_submit_claim()

        self.log_test_step("Step 2: Verify validation errors are displayed")
        validation_errors = self.claim_page.get_validation_errors()
        self.assert_true(len(validation_errors) > 0,
                         "Validation errors should be displayed for missing required fields")

        self.log_test_step("Step 3: Verify specific required field errors")
        # Check for required field indicators
        has_patient_error = self.claim_page.has_required_field_error("patientName")
        has_policy_error = self.claim_page.has_required_field_error("policyNumber")

        self.soft_assert_equals(has_patient_error, True,
                                "Patient name should show required error")
        self.soft_assert_equals(has_policy_error, True,
                                "Policy number should show required error")

    @allure.title("Test medical claim submission")
    @allure.description("Verify user can submit a medical claim")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_submit_medical_claim(self):
        """Test medical claim submission"""
        self.log_test_step("Step 1: Prepare medical claim data")
        claim_data = self._generate_test_claim_data(claim_type="Medical")

        self.log_test_step("Step 2: Submit medical claim")
        self.claim_page.submit_claim(claim_data)

        self.log_test_step("Step 3: Verify submission")
        self.claim_page.wait_for_page_load(timeout=15000)

        success_message = self.claim_page.get_success_message()
        self.assert_contains(success_message, "success",
                             "Success message should be displayed")

    @allure.title("Test dental claim submission")
    @allure.description("Verify user can submit a dental claim")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_submit_dental_claim(self):
        """Test dental claim submission"""
        self.log_test_step("Step 1: Prepare dental claim data")
        claim_data = self._generate_test_claim_data(claim_type="Dental")

        self.log_test_step("Step 2: Submit dental claim")
        self.claim_page.submit_claim(claim_data)

        self.log_test_step("Step 3: Verify submission")
        self.claim_page.wait_for_page_load(timeout=15000)

        is_submitted = self.claim_page.is_claim_submitted()
        self.assert_true(is_submitted, "Dental claim should be submitted successfully")

    @allure.title("Test vision claim submission")
    @allure.description("Verify user can submit a vision claim")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_submit_vision_claim(self):
        """Test vision claim submission"""
        self.log_test_step("Step 1: Prepare vision claim data")
        claim_data = self._generate_test_claim_data(claim_type="Vision")

        self.log_test_step("Step 2: Submit vision claim")
        self.claim_page.submit_claim(claim_data)

        self.log_test_step("Step 3: Verify submission")
        self.claim_page.wait_for_page_load(timeout=15000)

        is_submitted = self.claim_page.is_claim_submitted()
        self.assert_true(is_submitted, "Vision claim should be submitted successfully")

    @allure.title("Test claim submission with receipt upload")
    @allure.description("Verify user can submit a claim with receipt attachment")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_claim_submission_with_receipt(self):
        """Test claim submission with receipt upload"""
        self.log_test_step("Step 1: Prepare test claim data")
        claim_data = self._generate_test_claim_data()

        self.log_test_step("Step 2: Create test receipt file")
        # Create a dummy receipt file for testing
        test_receipt_path = Path("test_data") / "receipts" / "test_receipt.pdf"
        test_receipt_path.parent.mkdir(parents=True, exist_ok=True)

        if not test_receipt_path.exists():
            test_receipt_path.write_text("Test Receipt Content")

        self.log_test_step("Step 3: Submit claim with receipt")
        self.claim_page.submit_claim(claim_data, receipt_path=str(test_receipt_path))

        self.log_test_step("Step 4: Verify successful submission")
        self.claim_page.wait_for_page_load(timeout=15000)

        is_submitted = self.claim_page.is_claim_submitted()
        self.assert_true(is_submitted,
                         "Claim with receipt should be submitted successfully")

    @allure.title("Test save claim as draft")
    @allure.description("Verify user can save claim as draft without submitting")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_save_claim_as_draft(self):
        """Test save claim as draft"""
        self.log_test_step("Step 1: Fill partial claim information")
        claim_data = self._generate_test_claim_data()

        self.claim_page.select_claim_type(claim_data['claim_type'])
        self.claim_page.enter_patient_name(claim_data['patient_name'])
        self.claim_page.enter_policy_number(claim_data['policy_number'])

        self.log_test_step("Step 2: Save as draft")
        self.claim_page.click_save_draft()

        self.log_test_step("Step 3: Verify draft saved successfully")
        self.claim_page.wait_for_page_load(timeout=10000)

        success_message = self.claim_page.get_success_message()
        self.assert_contains(success_message.lower(), "draft",
                             "Draft save confirmation should be displayed")

    @allure.title("Test cancel claim submission")
    @allure.description("Verify user can cancel claim submission")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_cancel_claim_submission(self):
        """Test cancel claim submission"""
        self.log_test_step("Step 1: Fill some claim information")
        self.claim_page.enter_patient_name(self.faker.name())
        self.claim_page.enter_policy_number(f"BC{self.faker.random_number(digits=8)}")

        self.log_test_step("Step 2: Click cancel button")
        self.claim_page.click_cancel()

        self.log_test_step("Step 3: Verify navigation away from form")
        self.claim_page.wait_for_page_load(timeout=10000)

        # Verify we're no longer on the claim form
        form_displayed = self.claim_page.is_form_displayed()
        self.assert_false(form_displayed,
                          "Should navigate away from claim form after cancel")

    @allure.title("Test invalid claim amount")
    @allure.description("Verify validation for invalid claim amount")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_invalid_claim_amount(self):
        """Test invalid claim amount validation"""
        self.log_test_step("Step 1: Prepare claim data with invalid amount")
        claim_data = self._generate_test_claim_data()
        claim_data['claim_amount'] = "invalid_amount"

        self.log_test_step("Step 2: Fill form with invalid amount")
        self.claim_page.select_claim_type(claim_data['claim_type'])
        self.claim_page.enter_patient_name(claim_data['patient_name'])
        self.claim_page.enter_policy_number(claim_data['policy_number'])
        self.claim_page.enter_service_date(claim_data['service_date'])
        self.claim_page.enter_provider_name(claim_data['provider_name'])
        self.claim_page.enter_claim_amount(claim_data['claim_amount'])

        self.log_test_step("Step 3: Try to submit claim")
        self.claim_page.agree_to_terms()
        self.claim_page.confirm_accuracy()
        self.claim_page.click_submit_claim()

        self.log_test_step("Step 4: Verify validation error")
        validation_errors = self.claim_page.get_validation_errors()
        self.assert_true(len(validation_errors) > 0,
                         "Validation error should be displayed for invalid amount")

    @allure.title("Test invalid date format")
    @allure.description("Verify validation for invalid service date format")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_invalid_date_format(self):
        """Test invalid date format validation"""
        self.log_test_step("Step 1: Prepare claim data with invalid date")
        claim_data = self._generate_test_claim_data()
        claim_data['service_date'] = "invalid-date"

        self.log_test_step("Step 2: Fill form with invalid date")
        self.claim_page.select_claim_type(claim_data['claim_type'])
        self.claim_page.enter_patient_name(claim_data['patient_name'])
        self.claim_page.enter_policy_number(claim_data['policy_number'])
        self.claim_page.enter_service_date(claim_data['service_date'])
        self.claim_page.enter_provider_name(claim_data['provider_name'])
        self.claim_page.enter_claim_amount(claim_data['claim_amount'])

        self.log_test_step("Step 3: Try to submit claim")
        self.claim_page.agree_to_terms()
        self.claim_page.confirm_accuracy()
        self.claim_page.click_submit_claim()

        self.log_test_step("Step 4: Verify validation error")
        validation_errors = self.claim_page.get_validation_errors()
        self.assert_true(len(validation_errors) > 0,
                         "Validation error should be displayed for invalid date")

    @allure.title("Test terms and conditions requirement")
    @allure.description("Verify claim cannot be submitted without agreeing to terms")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_terms_conditions_required(self):
        """Test terms and conditions checkbox requirement"""
        self.log_test_step("Step 1: Fill all required fields except terms")
        claim_data = self._generate_test_claim_data()

        self.claim_page.select_claim_type(claim_data['claim_type'])
        self.claim_page.enter_patient_name(claim_data['patient_name'])
        self.claim_page.enter_policy_number(claim_data['policy_number'])
        self.claim_page.enter_service_date(claim_data['service_date'])
        self.claim_page.enter_provider_name(claim_data['provider_name'])
        self.claim_page.enter_claim_amount(claim_data['claim_amount'])
        self.claim_page.confirm_accuracy()

        self.log_test_step("Step 2: Try to submit without agreeing to terms")
        self.claim_page.click_submit_claim()

        self.log_test_step("Step 3: Verify validation error")
        validation_errors = self.claim_page.get_validation_errors()
        error_message = self.claim_page.get_error_message()

        # Check if either validation errors or error message indicates terms requirement
        self.assert_true(len(validation_errors) > 0 or "terms" in error_message.lower(),
                         "Error should indicate terms must be accepted")

    @allure.title("Test claim with maximum allowed amount")
    @allure.description("Verify claim submission with maximum allowed amount")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_claim_with_max_amount(self):
        """Test claim submission with maximum allowed amount"""
        self.log_test_step("Step 1: Prepare claim with maximum amount")
        claim_data = self._generate_test_claim_data()
        claim_data['claim_amount'] = "50000"  # Assuming max limit

        self.log_test_step("Step 2: Submit claim")
        self.claim_page.submit_claim(claim_data)

        self.log_test_step("Step 3: Verify submission or validation")
        self.claim_page.wait_for_page_load(timeout=15000)

        # Check if submission succeeded or validation error for exceeding limit
        is_submitted = self.claim_page.is_claim_submitted()
        error_message = self.claim_page.get_error_message()

        # Either submission succeeds or proper validation error is shown
        self.assert_true(is_submitted or "amount" in error_message.lower(),
                         "Claim with max amount should be handled appropriately")

    @allure.title("Test verify claim in claims history")
    @allure.description("Verify submitted claim appears in claims history")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_verify_claim_in_history(self):
        """Test claim appears in claims history after submission"""
        self.log_test_step("Step 1: Submit a claim")
        claim_data = self._generate_test_claim_data()
        self.claim_page.submit_claim(claim_data)

        self.log_test_step("Step 2: Wait for submission to complete")
        self.claim_page.wait_for_page_load(timeout=15000)

        # Get claim number
        claim_number = self.claim_page.get_claim_number()

        self.log_test_step("Step 3: Navigate to claims history")
        self.claim_page.navigate_to_my_claims()

        self.log_test_step("Step 4: Verify claim appears in history")
        # Verify recent claim status is visible
        claim_status = self.claim_page.get_recent_claim_status()
        self.assert_is_not_none(claim_status, "Claim status should be displayed")

        # Take screenshot for evidence
        self.take_screenshot("Claim_History_Verification")

    @allure.title("Test clear form functionality")
    @allure.description("Verify form fields can be cleared")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_clear_form_fields(self):
        """Test clearing form fields"""
        self.log_test_step("Step 1: Fill form with data")
        claim_data = self._generate_test_claim_data()

        self.claim_page.enter_patient_name(claim_data['patient_name'])
        self.claim_page.enter_policy_number(claim_data['policy_number'])
        self.claim_page.enter_service_date(claim_data['service_date'])

        self.log_test_step("Step 2: Clear all fields")
        self.claim_page.clear_all_fields()

        self.log_test_step("Step 3: Verify fields are cleared")
        patient_name = self.claim_page.get_attribute(
            self.claim_page.PATIENT_NAME_INPUT, "value"
        )
        self.assert_equals(patient_name, "", "Patient name field should be empty")

    @allure.title("Test prescription claim submission")
    @allure.description("Verify user can submit a prescription claim")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_submit_prescription_claim(self):
        """Test prescription claim submission"""
        self.log_test_step("Step 1: Prepare prescription claim data")
        claim_data = self._generate_test_claim_data(claim_type="Prescription")

        self.log_test_step("Step 2: Submit prescription claim")
        self.claim_page.submit_claim(claim_data)

        self.log_test_step("Step 3: Verify submission")
        self.claim_page.wait_for_page_load(timeout=15000)

        is_submitted = self.claim_page.is_claim_submitted()
        self.assert_true(is_submitted,
                         "Prescription claim should be submitted successfully")

    @allure.title("Test multiple claims submission")
    @allure.description("Verify user can submit multiple claims in sequence")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.ui
    def test_submit_multiple_claims(self):
        """Test submitting multiple claims in sequence"""
        claim_types = ["Medical", "Dental", "Vision"]
        submitted_claims = []

        for claim_type in claim_types:
            self.log_test_step(f"Submitting {claim_type} claim")
            claim_data = self._generate_test_claim_data(claim_type=claim_type)

            self.claim_page.submit_claim(claim_data)
            self.claim_page.wait_for_page_load(timeout=15000)

            is_submitted = self.claim_page.is_claim_submitted()
            submitted_claims.append(is_submitted)

            # Navigate back to submit new claim if not the last iteration
            if claim_type != claim_types[-1]:
                self.claim_page.navigate_to_submit_claim()
                self.claim_page.wait_for_form_load()

        self.log_test_step("Verify all claims submitted successfully")
        self.assert_equals(sum(submitted_claims), len(claim_types),
                           f"All {len(claim_types)} claims should be submitted")