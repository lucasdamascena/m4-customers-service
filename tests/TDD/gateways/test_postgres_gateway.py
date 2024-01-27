import uuid
from typing import List

import pytest
from mockito import when, verify, ANY

from src.entities.models.customer_entity import Customer
from src.interfaces.gateways.customer_gateway_interface import ICustomerGateway
from tests.utils.customer_helper import CustomerHelper


class MockRepository(ICustomerGateway):
    def get_by_id(self, customer_id: uuid.UUID) -> Customer:
        pass

    def get_by_cpf(self, cpf: str) -> Customer:
        pass

    def get_all(self) -> List[Customer]:
        pass

    def create(self, customer_in: Customer) -> Customer:
        pass

    def update(self, customer_id: uuid.UUID, customer_in: Customer) -> Customer:
        pass

    def remove(self, customer_id: uuid.UUID) -> None:
        pass


customer_repo = MockRepository()


@pytest.fixture
def unstub():
    from mockito import unstub
    yield
    unstub()


@pytest.fixture
def generate_new_customer():
    return CustomerHelper.generate_customer_entity()


@pytest.fixture
def generate_updated_customer():
    return CustomerHelper.generate_updated_customer_entity()


@pytest.fixture
def generate_multiple_customers():
    return CustomerHelper.generate_multiple_customer_entities()


def test_should_allow_register_customer(generate_new_customer, unstub):
    customer = generate_new_customer

    when(customer_repo).create(ANY(Customer)).thenReturn(customer)

    created_customer = customer_repo.create(customer)

    verify(customer_repo, times=1).create(customer)

    assert type(created_customer) == Customer
    assert created_customer is not None
    assert created_customer == customer
    assert customer.customer_id == created_customer.customer_id
    assert customer.cpf == created_customer.cpf
    assert customer.first_name == created_customer.first_name
    assert customer.last_name == created_customer.last_name
    assert customer.email == created_customer.email
    assert customer.phone == created_customer.phone


def test_should_allow_retrieve_customer_by_id(generate_new_customer, unstub):
    customer = generate_new_customer
    customer_id = customer.customer_id

    when(customer_repo).get_by_id(ANY(uuid.UUID)).thenReturn(customer)

    retrieved_customer = customer_repo.get_by_id(customer_id)

    verify(customer_repo, times=1).get_by_id(customer_id)

    assert customer.customer_id == retrieved_customer.customer_id
    assert customer.cpf == retrieved_customer.cpf
    assert customer.first_name == retrieved_customer.first_name
    assert customer.last_name == retrieved_customer.last_name
    assert customer.email == retrieved_customer.email
    assert customer.phone == retrieved_customer.phone


def test_should_allow_retrieve_customer_by_cpf(generate_new_customer, unstub):
    customer = generate_new_customer
    customer_cpf = customer.cpf

    when(customer_repo).get_by_cpf(ANY(str)).thenReturn(customer)

    retrieved_customer = customer_repo.get_by_cpf(customer_cpf)

    verify(customer_repo, times=1).get_by_cpf(customer_cpf)

    assert customer.customer_id == retrieved_customer.customer_id
    assert customer.cpf == retrieved_customer.cpf
    assert customer.first_name == retrieved_customer.first_name
    assert customer.last_name == retrieved_customer.last_name
    assert customer.email == retrieved_customer.email
    assert customer.phone == retrieved_customer.phone


def test_should_allow_update_customer(generate_new_customer, generate_updated_customer, unstub):
    customer = generate_new_customer
    customer_id = customer.customer_id

    updated_customer = generate_updated_customer
    customer.first_name = updated_customer.first_name
    customer.last_name = updated_customer.last_name
    customer.email = updated_customer.email
    customer.phone = updated_customer.phone

    when(customer_repo).update(ANY(uuid.UUID), ANY(Customer)).thenReturn(customer)

    created_customer = customer_repo.update(customer_id, customer)

    verify(customer_repo, times=1).update(customer_id, customer)

    assert type(created_customer) == Customer
    assert created_customer is not None
    assert created_customer == customer
    assert customer.customer_id == created_customer.customer_id
    assert customer.cpf == created_customer.cpf
    assert customer.first_name == created_customer.first_name
    assert customer.last_name == created_customer.last_name
    assert customer.email == created_customer.email
    assert customer.phone == created_customer.phone


def test_should_allow_list_customers(generate_multiple_customers, unstub):
    customers_list = generate_multiple_customers

    when(customer_repo).get_all().thenReturn(customers_list)

    result = customer_repo.get_all()

    verify(customer_repo, times=1).get_all()

    assert type(result) == list
    assert len(result) == len(customers_list)
    for customer in customers_list:
        assert customer in result


def test_should_allow_remove_customer(unstub):
    customer_id = uuid.uuid4()

    when(customer_repo).remove(ANY(uuid.UUID)).thenReturn()

    customer_repo.remove(customer_id)

    verify(customer_repo, times=1).remove(customer_id)


