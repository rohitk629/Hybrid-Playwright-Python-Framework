"""
Submit Claim Step Definitions
"""
from behave import given, when, then
import allure


@when('I fill in claim details')
def step_fill_claim_details(context):
    """Fill in claim form with provided details"""
    for row in context.table:
        field = row['field']
        value = row['value']

        # Map field names to selectors
        field_selectors = {
            'claim_type': '#claim_type',
            'provider_name': '#provider_name',
            'service_date': '#service_date',
            'claim_amount': '#claim_amount',
            'description': '#description'
        }

        selector = field_selectors.get(field)
        if selector:
            context.browser_utility.page.fill(selector, value)
            context.logger.info(f"Filled {field} with {value}")


@when('I attach supporting document "{document_name}"')
def step_attach_document(context, document_name):
    """Attach supporting document to claim"""
    file_input = context.browser_utility.page.locator('#file_upload')
    file_path = f"test_data/files/{document_name}"
    file_input.set_input_files(file_path)
    context.logger.info(f"Attached document: {document_name}")


@when('I click the "{button_name}" button')
def step_click_button(context, button_name):
    """Click specified button"""
    button_selectors = {
        'Submit Claim': '#submit_claim_btn',
        'Cancel': '#cancel_btn',
        'Save Draft': '#save_draft_btn'
    }

    selector = button_selectors.get(button_name, f'button:has-text("{button_name}")')
    context.browser_utility.page.click(selector)
    context.logger.info(f"Clicked button: {button_name}")


@then('I should see a success message "{message}"')
def step_verify_success_message(context, message):
    """Verify success message is displayed"""
    success_locator = context.browser_utility.page.locator('.success-message')
    success_locator.wait_for(state='visible', timeout=10000)

    actual_message = success_locator.text_content()
    assert message in actual_message, \
        f"Expected '{message}' in success message, but got '{actual_message}'"
    context.logger.info(f"Success message verified: {message}")


@then('I should see an error message "{message}"')
def step_verify_error_message(context, message):
    """Verify error message is displayed"""
    error_locator = context.browser_utility.page.locator('.error-message')
    error_locator.wait_for(state='visible', timeout=10000)

    actual_message = error_locator.text_content()
    assert message in actual_message, \
        f"Expected '{message}' in error message, but got '{actual_message}'"
    context.logger.info(f"Error message verified: {message}")


@then('the claim should appear in "{list_name}" list')
def step_verify_claim_in_list(context, list_name):
    """Verify claim appears in specified list"""
    claims_list = context.browser_utility.page.locator(f'#{list_name.lower().replace(" ", "_")}')
    claims_list.wait_for(state='visible', timeout=10000)

    # Get the latest claim (first in list)
    latest_claim = claims_list.locator('.claim-item').first
    assert latest_claim.is_visible(), f"Claim should appear in {list_name}"
    context.logger.info(f"Claim verified in {list_name}")


@then('I should receive a claim reference number')
def step_verify_claim_reference(context):
    """Verify claim reference number is generated"""
    reference_locator = context.browser_utility.page.locator('.claim-reference')
    reference_locator.wait_for(state='visible', timeout=10000)

    reference_number = reference_locator.text_content()
    assert reference_number, "Claim reference number should be generated"
    context.claim_reference = reference_number
    context.logger.info(f"Claim reference number: {reference_number}")


@then('the claim should not be submitted')
def step_verify_claim_not_submitted(context):
    """Verify no claim was submitted"""
    # Check that no success message appears
    success_locator = context.browser_utility.page.locator('.success-message')
    assert not success_locator.is_visible(), "No success message should appear"
    context.logger.info("Verified claim was not submitted")


@when('I start filling claim details')
def step_start_filling_claim(context):
    """Start filling claim form"""
    context.browser_utility.page.fill('#claim_type', 'Medical')
    context.logger.info("Started filling claim details")


@then('I should see a confirmation dialog "{message}"')
def step_verify_confirmation_dialog(context, message):
    """Verify confirmation dialog appears"""
    dialog_locator = context.browser_utility.page.locator('.confirmation-dialog')
    dialog_locator.wait_for(state='visible', timeout=10000)

    dialog_text = dialog_locator.text_content()
    assert message in dialog_text, \
        f"Expected '{message}' in dialog, but got '{dialog_text}'"
    context.logger.info("Confirmation dialog verified")


@when('I confirm cancellation')
def step_confirm_cancellation(context):
    """Confirm cancellation action"""
    context.browser_utility.page.click('button:has-text("Yes")')  # or '.confirm-btn'
    context.logger.info("Confirmed cancellation")


@then('no claim should be submitted')
def step_verify_no_claim_submitted(context):
    """Verify no claim was created"""
    # This could check database or API to ensure no record was created
    # For now, just verify we're not on success page
    current_url = context.browser_utility.page.url
    assert 'success' not in current_url.lower(), \
        "Should not be on success page after cancellation"
    context.logger.info("Verified no claim was submitted after cancellation")