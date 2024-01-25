import uuid
from typing import Any

from fastapi import APIRouter, status, Depends

from src.api.errors.api_errors import APIErrorMessage
from src.config.errors import RepositoryError, ResourceNotFound
from src.controllers.customer_controller import CustomerController
from src.entities.schemas.customer_dto import CustomerDTOResponse, CreateCustomerDTO, \
    ChangeCustomerDTO, CustomerDTOListResponse
from src.utils import utils

router = APIRouter(tags=["Customers"])


@router.get(
    "/customers",
    response_model=CustomerDTOListResponse,
    status_code=status.HTTP_200_OK,
    # dependencies=[Depends(utils.verify_jwt)],
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def get_all_customers() -> dict:
    try:
        result = await CustomerController.get_all_customers()
    except Exception:
        raise RepositoryError.get_operation_failed()

    return result


@router.get(
    "/customers/cpf/{cpf}",
    response_model=CustomerDTOResponse,
    status_code=status.HTTP_200_OK,
    # dependencies=[Depends(utils.verify_jwt)],
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def get_customer_by_cpf(
    cpf: str
) -> Any:
    try:
        result = await CustomerController.get_customer_by_cpf(cpf)
    except ResourceNotFound:
        raise ResourceNotFound.get_operation_failed(f"No customer with cpf: {cpf}")
    except Exception:
        raise RepositoryError.get_operation_failed()

    return result


@router.get(
    "/customers/id/{customer_id}",
    response_model=CustomerDTOResponse,
    status_code=status.HTTP_200_OK,
    # dependencies=[Depends(utils.verify_jwt)],
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def get_customer_by_id(
    customer_id: uuid.UUID
) -> dict:
    try:
        result = await CustomerController.get_customer_by_id(customer_id)
    except ResourceNotFound:
        raise ResourceNotFound.get_operation_failed(f"No customer with id: {customer_id}")
    except Exception:
        raise RepositoryError.get_operation_failed()

    return result


@router.post(
    "/customers",
    response_model=CustomerDTOResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def create_customer(
    request: CreateCustomerDTO
) -> dict:
    try:
        result = await CustomerController.create_customer(request)
    except Exception as e:
        print(e)
        raise RepositoryError.save_operation_failed()

    return result


@router.put(
    "/customers/{customer_id}",
    response_model=CustomerDTOResponse,
    status_code=status.HTTP_200_OK,
    # dependencies=[Depends(utils.verify_jwt)],
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def change_customer_data(
    customer_id: uuid.UUID,
    request: ChangeCustomerDTO
) -> dict:
    try:
        result = await CustomerController.change_customer_data(customer_id, request)
    except Exception as e:
        print(e)
        raise RepositoryError.save_operation_failed()

    return result


@router.delete(
    "/customers/{customer_id}",
    status_code=status.HTTP_200_OK,
    # dependencies=[Depends(utils.verify_jwt)],
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def remove_customer(
    customer_id: uuid.UUID
) -> dict:
    try:
        await CustomerController.remove_customer(customer_id)
    except Exception as e:
        print(e)
        raise RepositoryError.save_operation_failed()

    return {"result": "Customer removed successfully"}

