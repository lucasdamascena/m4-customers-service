from sqlalchemy import Column, String, UUID

from src.external.postgresql_database import Base


class Customers(Base):
    customer_id = Column(UUID, primary_key=True, index=True)
    cpf = Column(String(14), nullable=True)
    first_name = Column(String(30), nullable=True)
    last_name = Column(String(30), nullable=True)
    email = Column(String(80), nullable=True)
    phone = Column(String(20), nullable=True)
