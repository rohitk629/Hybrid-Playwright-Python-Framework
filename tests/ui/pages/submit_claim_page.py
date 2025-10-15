"""
Submit Claim Page Object Model
Handles claim submission functionality for Blue Cross insurance portal
"""

from core.base.base_page import BasePage
import allure
from typing import Optional


class SubmitClaimPage(BasePage):
    """Submit Claim page object"""

    # Navigation Locators
    CLAIMS_MENU = "//div[@id='b2-b10-Menu']"
    SUBMIT_CLAIM_LINK = "//div[@id='b2-b10-Items']//a[@role='menuitem'][normalize-space()='SUBMIT A CLAIM']"

    # Claim Form Locators
    CLAIM_CARDS = "//div[@class='list list-group OSFillParent']"
    CLAIM_TO_SELECT = "//div[@class='claim-card-label text-align-center']/span[text()='temp']"
    claimToSelect = ""
    CLAIM_CONTENT_TITLE = "//div[@id='b1-Title']/span"
    DATE_OF_SERVICE_INPUT = "//input[@aria-label='Select a date.']"
    FULL_COST = "//input[@id='b11-Input_FullCost']"
    AMOUNT_PAID_ANOTHER_POLICY  = "//input[@id='b11-Input_AmountPaidAnotherPolicy']"
    AMOUNT_PAID_GOVT_PROGRAM = "//input[@id='b11-Input_AmountPaidGovernment']"
    NEXT_BUTTON = "//button[@class='btn btn-primary width-5 OSFillParent']"
    PATIENT_NAME_INPUT = "#patientName"
    POLICY_NUMBER_INPUT = "#policyNumber"
    SERVICE_DATE_INPUT = "#serviceDate"
    PROVIDER_NAME_INPUT = "#providerName"
    CLAIM_AMOUNT_INPUT = "#claimAmount"
    DESCRIPTION_TEXTAREA = "#claimDescription"
    RECEIPT_UPLOAD_INPUT = "#receiptUpload"

    # Radio Buttons
    RADIO_INJURY_YES = "//input[@name='b11-RadioGroup_IsInjury'][@value='1']"
    RADIO_INJURY_NO = "//input[@name='b11-RadioGroup_IsInjury'][@value='0']"
    RADIO_HAS_ANOTHER_CLAIM_YES = "//input[@name='b11-RadioGroup_HasPortion'][@value='1']"
    RADIO_HAS_ANOTHER_CLAIM_NO = "//input[@name='b11-RadioGroup_HasPortion'][@value='0']"

    # Checkboxes
    TERMS_CHECKBOX = "#agreeTerms"
    CONFIRM_CHECKBOX = "#confirmAccuracy"

    # Buttons
    SUBMIT_BUTTON = "//button[contains(text(), 'Submit Claim')]"
    CANCEL_BUTTON = "//button[contains(text(), 'Cancel')]"
    SAVE_DRAFT_BUTTON = "//button[contains(text(), 'Save as Draft')]"

    # Validation and Success Messages
    WORKPLACE_INJURY_MESSAGE = "//div[@class='text-error']"
    SUCCESS_MESSAGE = "//div[@class='alert alert-success']"
    ERROR_MESSAGE = "//div[@class='alert alert-danger']"
    VALIDATION_ERROR = "//span[@class='field-validation-error']"
    CLAIM_NUMBER = "//div[@id='claimNumber']"
    CONFIRMATION_PAGE = "//h2[contains(text(), 'Claim Submitted')]"

    # Required Field Indicators
    REQUIRED_FIELD_ERROR = "//span[@class='text-danger']"

    # Claim History
    MY_CLAIMS_LINK = "//a[contains(text(), 'My Claims')]"
    CLAIM_STATUS = "//td[@class='claim-status']"
    RECENT_CLAIM = "(//tr[@class='claim-row'])[1]"


    @allure.step("Navigate to Submit Claim page")
    def navigate_to_submit_claim(self):
        """Navigate to submit claim page from main menu"""
        self.click(self.CLAIMS_MENU, timeout=15000)
        self.click(self.SUBMIT_CLAIM_LINK, timeout=10000)
        self.wait_for_page_load()

    @allure.step("Select claim type: {claim_type}")
    def select_claim_type(self, claim_type: str):
        """
        Select claim type from the claim card list

        Args:
            claim_type: Type of claim (e.g., 'Ambulance', 'Dental', 'EHB', 'Prescription drugs')
        """
        claim_to_select  = self.CLAIM_TO_SELECT.replace("temp", claim_type)
        self.click(claim_to_select)

    @allure.step("Wait for Claim content title to be visible")
    def wait_for_content_title(self, timeout):
        self.wait_for_specific_time(10)  # Wait for 3 seconds to allow content to load
        self.wait_for_element(self.CLAIM_CONTENT_TITLE, timeout=timeout)

    @allure.step("Get Claim content title")
    def get_content_title(self):
        """Get the Claim content title text"""
        return self.get_text(self.CLAIM_CONTENT_TITLE)

    @allure.step("Select 'Yes' for workplace injury radio button")
    def select_workplace_injury(self):
        """Select 'Yes' for workplace injury radio button"""
        self.click(self.RADIO_INJURY_YES)

    @allure.step("Get the displayed error message for workplace injury")
    def get_injury_error_message(self):
        """Get the Claim content title text"""
        return self.get_text(self.WORKPLACE_INJURY_MESSAGE)

    @allure.step("Enter patient name: {patient_name}")
    def enter_patient_name(self, patient_name: str):
        """Enter patient name"""
        self.enter_text(self.PATIENT_NAME_INPUT, patient_name)

    @allure.step("Enter policy number: {policy_number}")
    def enter_policy_number(self, policy_number: str):
        """Enter policy number"""
        self.enter_text(self.POLICY_NUMBER_INPUT, policy_number)

    @allure.step("Enter service date: {service_date}")
    def enter_service_date(self, service_date: str):
        """
        Enter service date

        Args:
            service_date: Date in format MM/DD/YYYY
        """
        self.enter_text(self.SERVICE_DATE_INPUT, service_date)

    @allure.step("Enter provider name: {provider_name}")
    def enter_provider_name(self, provider_name: str):
        """Enter healthcare provider name"""
        self.enter_text(self.PROVIDER_NAME_INPUT, provider_name)

    @allure.step("Enter claim amount: ${amount}")
    def enter_claim_amount(self, amount: str):
        """Enter claim amount"""
        self.enter_text(self.CLAIM_AMOUNT_INPUT, amount)

    @allure.step("Enter claim description")
    def enter_description(self, description: str):
        """Enter claim description"""
        self.enter_text(self.DESCRIPTION_TEXTAREA, description)

    @allure.step("Upload receipt file")
    def upload_receipt(self, file_path: str):
        """
        Upload receipt file

        Args:
            file_path: Path to receipt file
        """
        self.upload_file(self.RECEIPT_UPLOAD_INPUT, file_path)

    @allure.step("Agree to terms and conditions")
    def agree_to_terms(self):
        """Check terms and conditions checkbox"""
        self.check_checkbox(self.TERMS_CHECKBOX)

    @allure.step("Confirm claim accuracy")
    def confirm_accuracy(self):
        """Check accuracy confirmation checkbox"""
        self.check_checkbox(self.CONFIRM_CHECKBOX)

    @allure.step("Click Submit Claim button")
    def click_submit_claim(self):
        """Click submit claim button"""
        self.click(self.SUBMIT_BUTTON)

    @allure.step("Click Save as Draft button")
    def click_save_draft(self):
        """Click save draft button"""
        self.click(self.SAVE_DRAFT_BUTTON)

    @allure.step("Click Cancel button")
    def click_cancel(self):
        """Click cancel button"""
        self.click(self.CANCEL_BUTTON)

    @allure.step("Submit complete claim form")
    def submit_claim(self, claim_data: dict, receipt_path: Optional[str] = None):
        """
        Submit claim with all required information

        Args:
            claim_data: Dictionary containing claim information
            receipt_path: Optional path to receipt file
        """
        self.select_claim_type(claim_data.get('claim_type', 'Medical'))
        self.enter_patient_name(claim_data.get('patient_name'))
        self.enter_policy_number(claim_data.get('policy_number'))
        self.enter_service_date(claim_data.get('service_date'))
        self.enter_provider_name(claim_data.get('provider_name'))
        self.enter_claim_amount(claim_data.get('claim_amount'))

        if claim_data.get('description'):
            self.enter_description(claim_data.get('description'))

        if receipt_path:
            self.upload_receipt(receipt_path)

        self.agree_to_terms()
        self.confirm_accuracy()
        self.click_submit_claim()

    @allure.step("Get success message")
    def get_success_message(self) -> str:
        """Get success message text"""
        self.wait_for_element(self.SUCCESS_MESSAGE, timeout=10000)
        return self.get_text(self.SUCCESS_MESSAGE)

    @allure.step("Get error message")
    def get_error_message(self) -> str:
        """Get error message text"""
        if self.is_element_visible(self.ERROR_MESSAGE, timeout=5000):
            return self.get_text(self.ERROR_MESSAGE)
        return ""

    @allure.step("Get validation errors")
    def get_validation_errors(self) -> list:
        """Get all validation error messages"""
        errors = []
        if self.is_element_visible(self.VALIDATION_ERROR, timeout=2000):
            error_elements = self.get_all_texts(self.VALIDATION_ERROR)
            errors = [error for error in error_elements if error]
        return errors

    @allure.step("Get claim number")
    def get_claim_number(self) -> str:
        """Get submitted claim number"""
        self.wait_for_element(self.CLAIM_NUMBER, timeout=10000)
        return self.get_text(self.CLAIM_NUMBER)

    @allure.step("Check if claim submitted successfully")
    def is_claim_submitted(self) -> bool:
        """Check if claim was submitted successfully"""
        return self.is_element_visible(self.CONFIRMATION_PAGE, timeout=10000)

    @allure.step("Navigate to My Claims")
    def navigate_to_my_claims(self):
        """Navigate to My Claims page"""
        self.click(self.MY_CLAIMS_LINK)
        self.wait_for_page_load()

    @allure.step("Get recent claim status")
    def get_recent_claim_status(self) -> str:
        """Get status of most recent claim"""
        self.navigate_to_my_claims()
        return self.get_text(self.CLAIM_STATUS)

    @allure.step("Verify required field error for: {field_name}")
    def has_required_field_error(self, field_name: str) -> bool:
        """
        Check if a specific field shows required error

        Args:
            field_name: Name of the field to check

        Returns:
            True if required error is shown
        """
        error_locator = f"//input[@id='{field_name}']/following-sibling::span[@class='text-danger']"
        return self.is_element_visible(error_locator, timeout=2000)

    @allure.step("Clear all form fields")
    def clear_all_fields(self):
        """Clear all form fields"""
        self.clear_text(self.PATIENT_NAME_INPUT)
        self.clear_text(self.POLICY_NUMBER_INPUT)
        self.clear_text(self.SERVICE_DATE_INPUT)
        self.clear_text(self.PROVIDER_NAME_INPUT)
        self.clear_text(self.CLAIM_AMOUNT_INPUT)
        self.clear_text(self.DESCRIPTION_TEXTAREA)

    @allure.step("Wait for form to load")
    def wait_for_form_load(self):
        """Wait for claim form to fully load"""
        self.wait_for_element(self.CLAIM_CARDS, timeout=15000)
        self.wait_for_page_load()

    @allure.step("Check if form is displayed")
    def is_form_displayed(self) -> bool:
        """Check if claim form is displayed"""
        return self.is_element_visible(self.CLAIM_TYPE_DROPDOWN, timeout=5000)





