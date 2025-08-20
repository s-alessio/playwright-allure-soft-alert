# Soft assertions in Allure reports

This project demonstrates how to implement soft assertions in Playwright (using the Page Factory approach) and how to report them in Allure.

Soft assertions are assertions that allow a test to continue running even after an error occurs. 
They are useful when multiple similar checks are made in a single test. 
For example, if several texts on a page differ from the expected values, a hard assertion will stop at the first mismatch, but soft assertions will let you capture all of them in one run.

Goals of this project:
1. Implement soft assertions in the test automation framework.
2. Mark tests where soft assertion failures occurred as failed in the Allure report.
3. Include detailed error information about each soft assertion in the Allure report for easier debugging.

In the Page Factory approach, used alongside the Page Object and Page Component patterns, 
basic element actions are redefined in dedicated wrapper classes. 

For example, instead of doing
```python
await page.locator("...").click()
```
we can create object BasicElement and redefine click action in it:
```python
class BaseElement:
    def __init__(self, root: Union[Locator, FrameLocator], locator: str, name: str):
        """

        :param root: - part of webpage (Frame, for example) in which the locator is searched . If the locator is searched over all webpage root can be set to page.locator("body")
        :param locator: - locator of element
        :param name: name of element
        """
        self.root = root
        self.name = name
        self.locator = locator

    @property
    def type_of(self) -> str:
        return "base element"

    async def get_locator(self, nth: int = 0, **kwargs) -> Locator:
        locator = self.locator.format(**kwargs)
        step = f'Getting locator with "{locator}" at index "{nth}"'
        with allure.step(step):
            return self.root.locator(locator).nth(nth)
    
    def check_have_text(self, text: str, nth: int = 0, **kwargs):
        step = f'Checking that {self.type_of} "{self.name}" has text "{text}"'
        with allure.step(step):
            locator = await self.get_locator(nth, **kwargs)
            await expect(locator).to_have_text(text)
            
    async def click(self, nth: int = 0, **kwargs):
        step = f'Clicking {self.type_of} "{self.name}"'
        with allure.step(step):
            locator = await self.get_locator(nth, **kwargs)
            await locator.click()
```

This lets us easily add logging, waits, and error processing across all elements at once.

## Soft assertions implementation:
1. Mark tests that should use soft assertions:
```python
import pytest

@pytest.mark.soft
async def test_example(...):
    ...
```
2. Soft assertions state and verification (soft_allure.py):
```python
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
```
3. Enable soft mode per test (conftest.py):
```python
@pytest.fixture(autouse=True)
async def before_each_test(request):
    markers = request.node.iter_markers()
    marker_names = [m.name for m in markers]
    if "soft" in marker_names:
        soft_allure.safe_assert = True
```
4. Make element checks soft-aware:
```python
    async def check_have_text(self, text: str, nth: int = 0, **kwargs):
        step = f'Checking that {self.type_of} of "{self.name}" has text "{text}"'
        with allure.step(step):
            locator = await self.get_locator(nth, **kwargs)
            try:
                expect(locator).to_have_text(text)
            except AssertionError as e:
                if soft_allure.safe_assert:
                    msg = f"{step}: {e}"
                    soft_allure.safe_errors.append(msg)
                    soft_allure.attach_text_to_failed_step(str(e), attach_name="Soft assertion")
                else:
                    raise
            except Exception:
                raise
```

If test with soft_allure.safe_assert=True fails in this check AssertionError is not raised, 
error message is appended to soft_allure.safe_errors, and error is attached to current step as text.

5. Flush soft errors after the test, on teardown
```python
@pytest.fixture(autouse=True)
async def after_each_test(request):
    
    yield

    if soft_allure.safe_assert:
        with allure.step("Let's process soft asserts"):
            error_report = await soft_allure.verify_all(request.node)

        rep_soft = getattr(request.node, "rep_soft", None)

        if rep_soft and rep_soft == "failed":
            raise AssertionError(error_report)
```

With this setup, tests marked @pytest.mark.soft collect all assertion errors, attach them into Allure, and finally fail the test with a summarized report. 

How it appears in Allure reports:
1. Tests with soft-assert failures are marked Failed.
2. The steps where the failures occurred remain Passed (green) because the assertions were collected softly; each such step includes an attachment with the error details.
3. The test includes a final summary attachment listing all soft-assert failures captured during the run.
