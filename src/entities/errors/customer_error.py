from src.config.errors import DomainError, ResourceNotFound


class CustomerError(DomainError):
    @classmethod
    def invalid_cpf(cls) -> "CustomerError":
        return cls("Provided cpf is not valid!")


class CustomerNotFound(ResourceNotFound):
    pass
