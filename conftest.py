# conftest.py
import datetime
from utils.utils import append_result, generate_html_report
import os

test_results = []

def pytest_runtest_setup(item):
    """Record start time for each test."""
    item.start_time = datetime.datetime.now()

def pytest_runtest_makereport(item, call):
    """Append test result with status, message, payload, and execution time."""
    if call.when == "call":
        start_time = getattr(item, "start_time", datetime.datetime.now())
        end_time = datetime.datetime.now()
        exec_time = (end_time - start_time).total_seconds()
        
        # Get payload attached from test steps
        payload = getattr(item, "payload", "N/A")
        
        if call.excinfo is None:
            append_result(
                test_results,
                item.name,
                "PASSED",
                "Test executed successfully. All assertions passed.",
                payload,
                start_time=start_time,
                end_time=end_time
            )
        else:
            error_message = str(call.excinfo.value)
            reason = f"Assertion Failed: {error_message}" if "assert" in error_message else f"Error Occurred: {error_message}"
            append_result(
                test_results,
                item.name,
                "FAILED",
                reason,
                payload,
                start_time=start_time,
                end_time=end_time
            )

def pytest_sessionfinish(session, exitstatus):
    """Generate an HTML report at the end of the test session with auto-incremented filename."""
    # Ensure reports folder exists
    os.makedirs("reports", exist_ok=True)

    # Find the next available report filename (report.html, report1.html, report2.html...)
    base_name = "report"
    i = 0
    while True:
        if i == 0:
            filename = f"reports/{base_name}.html"
        else:
            filename = f"reports/{base_name}{i}.html"
        if not os.path.exists(filename):
            break
        i += 1

    generate_html_report(test_results, filename=filename)
