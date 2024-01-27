import uuid
from typing import List

import pytest
from mockito import when, verify, ANY

from src.config.errors import ResourceNotFound
from src.entities.models.customer_entity import Customer
from src.interfaces.gateways.customer_gateway_interface import ICustomerGateway
from src.interfaces.use_cases.customer_usecase_interface import CustomerUseCaseInterface
from src.usecases.customer_usecase import CustomerUseCase
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


class MockUsecase(CustomerUseCaseInterface):
    pass


customer_repo = MockRepository()
customer_usecase = CustomerUseCase(customer_repo)


@pytest.fixture
def unstub():
    from mockito import unstub
    yield
    unstub()


@pytest.fixture
def generate_new_customer():
    return CustomerHelper.generate_customer_entity()


@pytest.fixture
def generate_new_customer_dto():
    return CustomerHelper.generate_customer_request()


@pytest.fixture
def generate_updated_customer_dto():
    return CustomerHelper.generate_updated_customer_data()


@pytest.fixture
def generate_updated_customer():
    return CustomerHelper.generate_updated_customer_entity()


@pytest.fixture
def generate_multiple_customers():
    return CustomerHelper.generate_multiple_customer_entities()


def test_should_allow_register_customer(generate_new_customer_dto, unstub):
    customer_dto = generate_new_customer_dto
    customer_entity = Customer.create(
        cpf=customer_dto.cpf,
        first_name=customer_dto.first_name,
        last_name=customer_dto.last_name,
        email=customer_dto.email,
        phone=customer_dto.phone,
    )

    when(customer_repo).create(ANY(Customer)).thenReturn(customer_entity)

    created_customer = customer_usecase.create(customer_dto)

    assert created_customer is not None
    assert created_customer == customer_entity
    assert customer_dto.cpf == created_customer.cpf
    assert customer_dto.first_name == created_customer.first_name
    assert customer_dto.last_name == created_customer.last_name
    assert customer_dto.email == created_customer.email
    assert customer_dto.phone == created_customer.phone


def test_should_allow_retrieve_customer_by_id(generate_new_customer_dto, unstub):
    customer = generate_new_customer_dto
    customer_id = uuid.uuid4()

    when(customer_repo).get_by_id(ANY(uuid.UUID)).thenReturn(customer)

    retrieved_customer = customer_usecase.get_by_id(customer_id)

    verify(customer_repo, times=1).get_by_id(customer_id)

    assert customer.cpf == retrieved_customer.cpf
    assert customer.first_name == retrieved_customer.first_name
    assert customer.last_name == retrieved_customer.last_name
    assert customer.email == retrieved_customer.email
    assert customer.phone == retrieved_customer.phone


def test_should_raise_exception_invalid_id(unstub):
    customer_id = uuid.uuid4()

    when(customer_repo).get_by_id(ANY(uuid.UUID)).thenReturn()

    try:
        customer_usecase.get_by_id(customer_id)
        assert False
    except ResourceNotFound:
        assert True

    verify(customer_repo, times=1).get_by_id(customer_id)


def test_should_raise_exception_invalid_cpf(unstub):
    customer_cpf = ""

    when(customer_repo).get_by_cpf(ANY(str)).thenReturn()

    try:
        customer_usecase.get_by_cpf(customer_cpf)
        assert False
    except ResourceNotFound:
        assert True

    verify(customer_repo, times=1).get_by_cpf(customer_cpf)


def test_should_allow_retrieve_customer_by_cpf(generate_new_customer_dto, unstub):
    customer = generate_new_customer_dto
    customer_cpf = customer.cpf

    when(customer_repo).get_by_cpf(ANY(str)).thenReturn(customer)

    retrieved_customer = customer_usecase.get_by_cpf(customer_cpf)

    verify(customer_repo, times=1).get_by_cpf(customer_cpf)

    assert customer.cpf == retrieved_customer.cpf
    assert customer.first_name == retrieved_customer.first_name
    assert customer.last_name == retrieved_customer.last_name
    assert customer.email == retrieved_customer.email
    assert customer.phone == retrieved_customer.phone


def test_should_allow_update_customer(generate_new_customer, generate_updated_customer_dto, generate_updated_customer, unstub):
    old_customer = generate_new_customer
    old_customer_id = old_customer.customer_id
    new_customer_data = generate_updated_customer_dto

    old_customer.first_name = new_customer_data.first_name
    old_customer.last_name = new_customer_data.last_name
    old_customer.email = new_customer_data.email
    old_customer.phone = new_customer_data.phone

    when(customer_repo).get_by_id(ANY(uuid.UUID)).thenReturn(old_customer)
    when(customer_repo).update(ANY(uuid.UUID), ANY(Customer)).thenReturn(old_customer)

    updated_customer = customer_usecase.update(old_customer_id, new_customer_data)

    assert updated_customer is not None
    assert updated_customer.first_name == old_customer.first_name
    assert updated_customer.last_name == old_customer.last_name
    assert updated_customer.email == old_customer.email
    assert updated_customer.phone == old_customer.phone


def test_should_allow_list_customers(generate_multiple_customers, unstub):
    customers_list = generate_multiple_customers

    when(customer_repo).get_all().thenReturn(customers_list)

    result = customer_usecase.get_all()

    verify(customer_repo, times=1).get_all()

    assert type(result) == list
    assert len(result) == len(customers_list)
    for customer in customers_list:
        assert customer in result


def test_should_allow_list_empty_customers(generate_multiple_customers, unstub):
    when(customer_repo).get_all().thenReturn(list())

    result = customer_usecase.get_all()

    assert result == list()
    verify(customer_repo, times=1).get_all()


def test_should_allow_remove_customer(unstub):
    customer_id = uuid.uuid4()

    when(customer_repo).remove(ANY(uuid.UUID)).thenReturn()

    customer_usecase.remove(customer_id)

    verify(customer_repo, times=1).remove(customer_id)
