import uuid
from typing import List, Optional, Type
from fastapi.encoders import jsonable_encoder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.config import settings
from src.entities.models.customer_entity import Customer, customer_factory
from src.gateways.orm.customer_orm import Customers
from src.interfaces.gateways.customer_gateway_interface import ICustomerGateway

connection_uri = settings.db.SQLALCHEMY_DATABASE_URI

engine = create_engine(
    connection_uri
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class PostgresDBCustomerRepository(ICustomerGateway):
    @staticmethod
    def to_entity(customer: Type[Customers]) -> Customer:
        customer = customer_factory(
            customer.customer_id,
            customer.cpf,
            customer.first_name,
            customer.last_name,
            customer.email,
            customer.phone,
        )
        return customer

    def get_by_id(self, customer_id: uuid.UUID) -> Optional[Customer]:
        with SessionLocal() as db:
            result = db.query(Customers).filter(Customers.customer_id == customer_id).first()
        if result:
            return self.to_entity(result)
        else:
            return None

    def get_by_cpf(self, cpf: str) -> Optional[Customer]:
        with SessionLocal() as db:
            result = db.query(Customers).filter(Customers.cpf == cpf).first()
        if result:
            return self.to_entity(result)
        else:
            return None

    def get_all(self) -> List[Customer]:
        customers = []

        with SessionLocal() as db:
            result = db.query(Customers).all()

        for customer in result:
            customers.append(self.to_entity(customer))

        return customers

    def create(self, obj_in: Customer) -> Customer:
        obj_in_data = jsonable_encoder(obj_in, by_alias=False)
        db_obj = Customers(**obj_in_data)  # type: ignore

        with SessionLocal() as db:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)

        new_customer = self.to_entity(db_obj)  # type: ignore
        return new_customer

    def update(self, customer_id: uuid.UUID, obj_in: Customer) -> Customer:
        customer_in = vars(obj_in)
        with SessionLocal() as db:
            db_obj = db.query(Customers).filter(Customers.customer_id == customer_id).first()
            obj_data = jsonable_encoder(db_obj, by_alias=False)
            for field in obj_data:
                if field in customer_in:
                    setattr(db_obj, field, customer_in[field])
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        updated_customer = self.to_entity(db_obj)
        return updated_customer

    def remove(self, customer_id: uuid.UUID) -> None:
        with SessionLocal() as db:
            db_obj = db.query(Customers).filter(Customers.customer_id == customer_id).first()
            db.delete(db_obj)
            db.commit()
