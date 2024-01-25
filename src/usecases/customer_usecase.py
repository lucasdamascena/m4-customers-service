import uuid

from src.config.errors import ResourceNotFound

from src.entities.schemas.customer_dto import CreateCustomerDTO, ChangeCustomerDTO
from src.entities.models.customer_entity import Customer
from src.interfaces.gateways.customer_gateway_interface import ICustomerGateway
from src.interfaces.use_cases.customer_usecase_interface import CustomerUseCaseInterface


class CustomerUseCase(CustomerUseCaseInterface):
    def __init__(self, customer_repo: ICustomerGateway) -> None:
        self._customer_repo = customer_repo

    def get_by_id(self, customer_id: uuid.UUID):
        result = self._customer_repo.get_by_id(customer_id)
        if not result:
            raise ResourceNotFound
        else:
            return result

    def get_by_cpf(self, cpf: str):
        result = self._customer_repo.get_by_cpf(cpf)
        if not result:
            raise ResourceNotFound
        else:
            return result

    def get_all(self):
        return self._customer_repo.get_all()

    def create(self, input_dto: CreateCustomerDTO) -> Customer:
        customer = Customer.create(
            input_dto.cpf,
            input_dto.first_name,
            input_dto.last_name,
            input_dto.email,
            input_dto.phone,
        )
        new_customer = self._customer_repo.create(customer)
        return new_customer

    def update(self, customer_id: uuid.UUID, input_dto: ChangeCustomerDTO) -> Customer:
        customer = self._customer_repo.get_by_id(customer_id)

        if input_dto.first_name:
            customer.change_first_name(input_dto.first_name)
        if input_dto.last_name:
            customer.change_last_name(input_dto.last_name)
        if input_dto.email:
            customer.change_email(input_dto.email)
        if input_dto.phone:
            customer.change_phone(input_dto.phone)

        updated_customer = self._customer_repo.update(customer_id, customer)
        return updated_customer

    def remove(self, customer_id: uuid.UUID) -> None:
        self._customer_repo.remove(customer_id)
