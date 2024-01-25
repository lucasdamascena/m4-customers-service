from typing import List

from src.entities.models.customer_entity import Customer
from src.utils.utils import camelize_dict


def customer_to_json(customer: Customer):
    return camelize_dict(customer.__dict__)


def customer_list_to_json(customer_list: List[Customer]):
    return [camelize_dict(customer.__dict__) for customer in customer_list]

