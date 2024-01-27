from typing import List

from src.entities.models.customer_entity import Customer
from src.entities.schemas.customer_dto import CreateCustomerDTO, ChangeCustomerDTO


class CustomerHelper:

    @staticmethod
    def generate_customer_request() -> CreateCustomerDTO:
        return CreateCustomerDTO(
            cpf="000.000.000-01",
            first_name="Zé",
            last_name="da Silva",
            email="email@email.com",
            phone="99999-9999"
        )

    @staticmethod
    def generate_multiple_customers() -> List[CreateCustomerDTO]:
        customers_list = []
        customer1 = CreateCustomerDTO(
            cpf="000.000.000-01",
            first_name="Zé",
            last_name="da Silva",
            email="email@email.com",
            phone="99999-9999"
        )

        customer2 = CreateCustomerDTO(
            cpf="000.000.000-02",
            first_name="Maria",
            last_name="da Silva",
            email="email2@email.com",
            phone="98888-8888"
        )
        customers_list.append(customer1)
        customers_list.append(customer2)
        return customers_list

    @staticmethod
    def generate_updated_customer_data() -> ChangeCustomerDTO:
        return ChangeCustomerDTO(
            first_name="Zé",
            last_name="da Silva Sauro",
            email="email_novo@email.com",
            phone="(11) 99999-9999"
        )

    @staticmethod
    def generate_customer_entity() -> Customer:
        return Customer.create(
            cpf="000.000.000-01",
            first_name="Zé",
            last_name="da Silva",
            email="email@email.com",
            phone="99999-9999"
        )

    @staticmethod
    def generate_updated_customer_entity() -> Customer:
        return Customer.create(
            cpf="000.000.000-01",
            first_name="Zé",
            last_name="da Silva Sauro",
            email="email_novo@email.com",
            phone="(11) 99999-9999"
        )

    @staticmethod
    def generate_multiple_customer_entities() -> List[Customer]:
        customers_list = []
        customer1 = Customer.create(
            cpf="000.000.000-01",
            first_name="Zé",
            last_name="da Silva",
            email="email@email.com",
            phone="99999-9999"
        )

        customer2 = Customer.create(
            cpf="000.000.000-02",
            first_name="Zé",
            last_name="da Silva",
            email="email@email.com",
            phone="99999-9999"
        )
        customers_list.append(customer1)
        customers_list.append(customer2)
        return customers_list
