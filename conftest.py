import os

import allure
import pytest
from allure_commons.types import AttachmentType

from tools import soft_allure

pytest_plugins = (
    "fixtures.pages",
    "fixtures.browsers"
)


@pytest.fixture(autouse=True)
async def before_each_test(request):
    markers = request.node.iter_markers()
    marker_names = [m.name for m in markers]
    if "soft" in marker_names:
        soft_allure.safe_assert = True

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)  # rep.when in {"setup","call","teardown"}



@pytest.fixture(autouse=True)
async def after_each_test(request):
    yield
    if soft_allure.safe_assert:
        with allure.step("Let's process soft asserts"):
            error_report = await soft_allure.verify_all(request.node)

    rep_setup = getattr(request.node, "rep_setup", None)
    rep_call = getattr(request.node, "rep_call", None)
    rep_soft = getattr(request.node, "rep_soft", None)

    failed_call = bool(rep_call and rep_call.failed and not getattr(rep_call, "wasxfail", False))
    failed_setup = bool(rep_setup and rep_setup.failed)

    if rep_soft and rep_soft == "failed":
        failed_soft = True
    else:
        failed_soft = False
    failed = failed_setup or failed_call or failed_soft

    trace_zip = getattr(request.node, "_allure_trace_zip", None)
    video_path = getattr(request.node, "_allure_video_path", None)

    if failed:
        try:
            if video_path and os.path.exists(video_path):
                allure.attach.file(video_path, name="video", attachment_type=AttachmentType.WEBM)
        except Exception:
            pass
        try:
            if trace_zip and os.path.exists(trace_zip):
                allure.attach.file(trace_zip, name="trace", extension="zip")
        except Exception:
            pass

        if failed_soft:
            raise AssertionError(error_report)

