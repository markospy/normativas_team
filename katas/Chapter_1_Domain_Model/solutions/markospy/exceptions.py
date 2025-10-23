class DomainError(Exception):
    pass


class NoAvailableVet(DomainError):
    """Excepción lanzada cuando no hay veterinarios disponibles."""

    message = "No available vet"

    def __init__(self, message: str = None):
        super().__init__(message or self.message)
