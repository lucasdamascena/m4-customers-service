import uuid
from dataclasses import dataclass


@dataclass
class Customer:
    customer_id: uuid.UUID
    cpf: str
    first_name: str
    last_name: str
    email: str
    phone: str

    @classmethod
    def create(cls, cpf: str, first_name: str, last_name: str, email: str, phone: str) -> "Customer":
        customer_id = uuid.uuid4()
        if not cpf and not first_name and not last_name and not email and not phone:
            first_name = "Visitante" + str(customer_id)[0:8]

        return cls(customer_id, cpf, first_name, last_name, email, phone)

    def change_first_name(self, new_first_name) -> None:
        self.first_name = new_first_name

    def change_last_name(self, new_last_name) -> None:
        self.last_name = new_last_name

    def change_email(self, new_email: str) -> None:
        self.email = new_email

    def change_phone(self, new_phone: str) -> None:
        self.phone = new_phone


def customer_factory(
     customer_id: uuid.UUID,
     cpf: str,
     first_name: str,
     last_name: str,
     email: str,
     phone: str
) -> Customer:
    return Customer(
        customer_id=customer_id,
        cpf=cpf,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
    )
