import allure

safe_assert = False
safe_errors = []

def attach_text_to_failed_step(text: str, attach_name: str = "Details"):
    allure.attach(text, name=attach_name, attachment_type=allure.attachment_type.TEXT)

async def verify_all(item):
    global safe_assert, safe_errors

    """Final check for all errors"""
    if len(safe_errors)>0 and safe_assert:
        # Creating report for Allure
        error_summary = f"Found {len(safe_errors)} soft assertion errors"
        detailed_errors = []

        for i, error in enumerate(safe_errors, 1):
            detailed_errors.append(f"{i}. {error}")

        full_report = f"{error_summary}:\n" + "\n".join(detailed_errors)

        # Attach report to Allure
        allure.attach(full_report, "Soft Assertions Summary", allure.attachment_type.TEXT)

        safe_assert = False
        safe_errors = []
        item.rep_soft = "failed"
        return full_report