import uuid
from typing import Any

from src.adapters.customer_json_adapter import customer_list_to_json, customer_to_json
from src.config.errors import ResourceNotFound, RepositoryError
from src.entities.schemas.customer_dto import CreateCustomerDTO, ChangeCustomerDTO
from src.gateways.postgres_gateways.customer_gateway import PostgresDBCustomerRepository
from src.usecases.customer_usecase import CustomerUseCase


class CustomerController:

    @staticmethod
    async def get_all_customers() -> dict:
        customer_gateway = PostgresDBCustomerRepository()

        try:
            all_customers = CustomerUseCase(customer_gateway).get_all()
            if all_customers:
                result = customer_list_to_json(all_customers)
            else:
                result = list()
        except Exception:
            raise RepositoryError.get_operation_failed()

        return {"result": result}

    @staticmethod
    async def get_customer_by_cpf(
        cpf: str
    ) -> Any:
        customer_gateway = PostgresDBCustomerRepository()

        try:
            customer = CustomerUseCase(customer_gateway).get_by_cpf(cpf)
            result = customer_to_json(customer)
        except ResourceNotFound:
            raise ResourceNotFound.get_operation_failed(f"No customer with cpf: {cpf}")
        except Exception:
            raise RepositoryError.get_operation_failed()

        return {"result": result}

    @staticmethod
    async def get_customer_by_id(
        customer_id: uuid.UUID
    ) -> dict:
        customer_gateway = PostgresDBCustomerRepository()

        try:
            customer = CustomerUseCase(customer_gateway).get_by_id(customer_id)
            result = customer_to_json(customer)
        except ResourceNotFound:
            raise ResourceNotFound.get_operation_failed(f"No customer with id: {customer_id}")
        except Exception:
            raise RepositoryError.get_operation_failed()

        return {"result": result}

    @staticmethod
    async def create_customer(
        request: CreateCustomerDTO
    ) -> dict:
        customer_gateway = PostgresDBCustomerRepository()

        try:
            customer = CustomerUseCase(customer_gateway).create(request)
            result = customer_to_json(customer)
        except Exception as e:
            print(e)
            raise RepositoryError.save_operation_failed()

        return {"result": result}

    @staticmethod
    async def change_customer_data(
        customer_id: uuid.UUID,
        request: ChangeCustomerDTO
    ) -> dict:
        customer_gateway = PostgresDBCustomerRepository()

        try:
            customer = CustomerUseCase(customer_gateway).update(customer_id, request)
            result = customer_to_json(customer)
        except Exception:
            raise RepositoryError.save_operation_failed()

        return {"result": result}

    @staticmethod
    async def remove_customer(
        customer_id: uuid.UUID
    ) -> dict:
        customer_gateway = PostgresDBCustomerRepository()

        try:
            CustomerUseCase(customer_gateway).remove(customer_id)
        except Exception:
            raise RepositoryError.save_operation_failed()

        return {"result": "Customer removed successfully"}

