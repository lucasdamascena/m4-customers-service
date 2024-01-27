import json

import pytest

from pytest_bdd import scenario, given, then, when
from starlette import status
from starlette.testclient import TestClient

from src.app import app
from tests.utils.customer_helper import CustomerHelper


client = TestClient(app)


@pytest.fixture
def generate_customer_dto():
    return CustomerHelper.generate_customer_request()


@pytest.fixture
def generate_multiple_customer_dtos():
    return CustomerHelper.generate_multiple_customers()


@pytest.fixture
def generate_update_customer_dto():
    return CustomerHelper.generate_updated_customer_data()


@pytest.fixture
def request_customer_creation(generate_customer_dto):
    customer = generate_customer_dto
    req_body = {
        "cpf": customer.cpf,
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "email": customer.email,
        "phone": customer.phone,
    }
    headers = {}
    response = client.post("/customers", json=req_body, headers=headers)

    resp_json = json.loads(response.content)
    result = resp_json["result"]
    customer_id = result["customerId"]

    yield response
    # Teardown - Removes the customer from the database
    client.delete(f"/customers/{customer_id}", headers=headers)


@pytest.fixture
def request_multiple_customers_creation(generate_multiple_customer_dtos):
    customers_list = generate_multiple_customer_dtos
    customer_ids_list = []
    headers = {}

    for customer in customers_list:
        req_body = {
            "cpf": customer.cpf,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "email": customer.email,
            "phone": customer.phone,
        }
        response = client.post("/customers", json=req_body, headers=headers)

        resp_json = json.loads(response.content)
        result = resp_json["result"]
        customer_id = result["customerId"]
        customer_ids_list.append(customer_id)
    yield customer_ids_list
    # Teardown - Removes the customer from the database
    for customer_id in customer_ids_list:
        client.delete(f"/customers/{customer_id}", headers=headers)


@pytest.fixture
def create_customer_without_teardown(generate_customer_dto):
    customer = generate_customer_dto
    req_body = {
        "cpf": customer.cpf,
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "email": customer.email,
        "phone": customer.phone,
    }
    headers = {}
    response = client.post("/customers", json=req_body, headers=headers)
    yield response.content


# Scenario: Create a new customer


@scenario('../customer.feature', 'Create a new customer')
def test_create_customer():
    pass


@given('I submit a new customer data', target_fixture='i_request_to_create_a_new_customer_impl')
def i_request_to_create_a_new_customer_impl(generate_customer_dto, request_customer_creation):
    response = request_customer_creation
    return response


@then('the customer should be created successfully')
def the_customer_should_be_created_successfully_impl(i_request_to_create_a_new_customer_impl, generate_customer_dto):
    customer = generate_customer_dto
    resp_json = json.loads(i_request_to_create_a_new_customer_impl.content)
    result = resp_json["result"]

    assert result["cpf"] == customer.cpf
    assert result["firstName"] == customer.first_name
    assert result["lastName"] == customer.last_name
    assert result["email"] == customer.email
    assert result["phone"] == customer.phone


# Scenario: Get customer by CPF

@scenario('../customer.feature', 'Get customer by CPF')
def test_get_customer_by_cpf():
    pass


@given('there is a customer with a specific CPF', target_fixture='customer_with_given_cpf')
def customer_with_given_cpf(request_customer_creation):
    customer = request_customer_creation
    return customer


@when('I request to get the customer by CPF', target_fixture='request_customer_by_cpf')
def request_customer_by_cpf(customer_with_given_cpf):
    customer_response = customer_with_given_cpf
    resp_json = json.loads(customer_response.content)
    customer_cpf = resp_json["result"]["cpf"]

    headers = {}
    response = client.get(f"/customers/cpf/{customer_cpf}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    return response.content


@then('I should receive the customer details by CPF')
def receive_given_customer(request_customer_by_cpf, generate_customer_dto):
    customer = generate_customer_dto
    resp_json = json.loads(request_customer_by_cpf)
    result = resp_json["result"]

    assert result["cpf"] == customer.cpf
    assert result["firstName"] == customer.first_name
    assert result["lastName"] == customer.last_name
    assert result["email"] == customer.email
    assert result["phone"] == customer.phone


# Scenario: Get customer by ID

@scenario('../customer.feature', 'Get customer by ID')
def test_get_customer_by_id():
    pass


@given('there is a customer with a specific ID', target_fixture='customer_with_given_id')
def customer_with_given_id(request_customer_creation):
    response = request_customer_creation
    resp_json = json.loads(response.content)
    result = resp_json["result"]
    return result["customerId"]


@when('I request to get the customer by ID', target_fixture='request_customer_by_id')
def request_customer_by_id(customer_with_given_id):
    customer_id = customer_with_given_id
    headers = {}
    response = client.get(f"/customers/id/{customer_id}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.content is not None

    return response.content


@then('I should receive the customer details by ID')
def receive_correct_customer(customer_with_given_id, request_customer_by_id, generate_customer_dto):
    customer_id = customer_with_given_id
    customer = generate_customer_dto
    resp_json = json.loads(request_customer_by_id)
    result = resp_json["result"]

    assert result["customerId"] == customer_id
    assert result["cpf"] == customer.cpf
    assert result["firstName"] == customer.first_name
    assert result["lastName"] == customer.last_name
    assert result["email"] == customer.email
    assert result["phone"] == customer.phone


# Scenario: Get all customers

@scenario('../customer.feature', 'Get all customers')
def test_get_all_customers():
    pass


@given('there are existing customers in the system', target_fixture='existing_customers_in_db')
def existing_customers_in_db(request_multiple_customers_creation):
    customers_id_list = request_multiple_customers_creation
    return customers_id_list


@when('I request to get all customers', target_fixture='request_all_customers')
def request_all_customers():
    headers = {}
    response = client.get(f"/customers/", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.content is not None

    return response.content


@then('I should receive a list of customers')
def receive_correct_customer(existing_customers_in_db, request_all_customers):
    customers_id_list = existing_customers_in_db
    response = request_all_customers
    resp_json = json.loads(response)
    result = resp_json["result"]

    assert type(result) == list

    for item in result:
        assert item["customerId"] in customers_id_list


# Scenario: Update customer data

@scenario('../customer.feature', 'Update customer data')
def test_update_customer():
    pass


@given('there is a registered customer', target_fixture='existing_customer')
def existing_customer(request_customer_creation):
    response = request_customer_creation
    resp_json = json.loads(response.content)
    result = resp_json["result"]
    return result


@when('I request to update a customer', target_fixture='request_customer_update')
def request_customer_update(existing_customer, generate_update_customer_dto):
    customer = existing_customer
    customer_id = customer["customerId"]

    updated_customer = generate_update_customer_dto
    req_body = {
        "first_name": updated_customer.first_name,
        "last_name": updated_customer.last_name,
        "email": updated_customer.email,
        "phone": updated_customer.phone,
    }

    headers = {}
    response = client.put(f"/customers/{customer_id}", json=req_body, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.content is not None

    return response.content


@then('the customer data is successfully updated')
def receive_correct_customer(request_customer_update, generate_update_customer_dto):
    updated_customer = generate_update_customer_dto

    response = request_customer_update
    resp_json = json.loads(response)
    result = resp_json["result"]

    assert result["firstName"] == updated_customer.first_name
    assert result["lastName"] == updated_customer.last_name
    assert result["email"] == updated_customer.email
    assert result["phone"] == updated_customer.phone


# Scenario: Remove a customer

@scenario('../customer.feature', 'Remove a customer')
def test_remove_customer():
    pass


@given('there is a customer on database with specific id', target_fixture='existing_customer_to_remove')
def existing_customer_to_remove(create_customer_without_teardown):
    customer = create_customer_without_teardown
    return customer


@when('I request to remove a customer', target_fixture='request_customer_update')
def request_customer_delete(existing_customer_to_remove):
    response = existing_customer_to_remove
    resp_json = json.loads(response)
    result = resp_json["result"]
    customer_id = result["customerId"]

    headers = {}
    response = client.delete(f"/customers/{customer_id}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.content is not None

    return response.content


@then('the customer data is successfully removed')
def receive_correct_customer(existing_customer_to_remove):
    response = existing_customer_to_remove
    resp_json = json.loads(response)
    result = resp_json["result"]
    customer_id = result["customerId"]

    headers = {}
    response = client.get(f"/customers/id/{customer_id}", headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
