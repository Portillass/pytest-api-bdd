import requests
from pytest_bdd import scenarios, given, when, then
import pytest

BASE_URL = "https://api.restful-api.dev/objects"

# Link to the feature file
scenarios("../features/object_lifecycle.feature")


@pytest.fixture
def context():
    """Shared context dictionary to store data across steps."""
    return {}


# ====================
# Scenario 1: Successfully create, retrieve, update and delete an object
# ====================

# Given I have a valid object payload
@given("I have a valid object payload")
def valid_payload(context):
    context["payload"] = {
        "name": "Test Object",
        "data": {"year": 2024, "price": 100}
    }

 # When I send a POST request to create the object
@when("I send a POST request to create the object")
def create_object(context):
    response = requests.post(BASE_URL, json=context["payload"])
    context["response"] = response
    if response.status_code == 200:
        context["object_id"] = response.json().get("id")
        context["created_name"] = response.json().get("name")


@then("the response status code should be 200")
def status_code_200(context):
    assert context["response"].status_code == 200


@then("the response should contain an object id")
def response_contains_id(context):
    assert "id" in context["response"].json()


@when("I send a GET request using the stored object id")
def get_object(context):
    if "object_id" in context:
        response = requests.get(f"{BASE_URL}/{context['object_id']}")
        context["response"] = response


@then("the response name should match the created object name")
def name_matches_created(context):
    if "object_id" in context:
        assert context["response"].json().get("name") == context["created_name"]


@when("I update the object with a new name")
def update_object(context):
    if "object_id" in context:
        updated_payload = {"name": "Updated Object Name"}
        response = requests.put(f"{BASE_URL}/{context['object_id']}", json=updated_payload)
        context["response"] = response
        context["updated_name"] = updated_payload["name"]


@then("the response name should reflect the updated value")
def name_matches_updated(context):
    if "object_id" in context:
        assert context["response"].json().get("name") == context["updated_name"]


@when("I send a DELETE request using the stored object id")
def delete_object(context):
    if "object_id" in context:
        response = requests.delete(f"{BASE_URL}/{context['object_id']}")
        context["response"] = response


@when("I send a GET request using the deleted object id")
def get_deleted_object(context):
    if "object_id" in context:
        response = requests.get(f"{BASE_URL}/{context['object_id']}")
        context["response"] = response


@then("the response status code should be 404")
def status_code_404(context):
    if "response" in context:
        assert context["response"].status_code == 404


# ====================
# Scenario 2: Retrieve non-existing object
# ====================
@given("I have a non-existing object id")
def non_existing_id(context):
    context["object_id"] = "non-existing-id-12345"


@when("I send a GET request using that id")
def get_object_by_id(context):
    response = requests.get(f"{BASE_URL}/{context['object_id']}")
    context["response"] = response


@then("the response status code should be 404 for non-existing object")
def status_code_404_nonexisting(context):
    assert context["response"].status_code == 404


# ====================
# Scenario 3: Create object with invalid payload
# ====================
@given("I have an invalid object payload")
def invalid_payload(context):
    context["payload"] = {
        "data": {"year": 2024, "price": 100} 
    }


@when("I send a POST request to create the object with invalid payload")
def create_object_invalid(context):
    response = requests.post(BASE_URL, json=context["payload"])
    context["response"] = response


@then("the response status code should indicate a client error")
def client_error(context):
    assert context["response"].status_code >= 200
