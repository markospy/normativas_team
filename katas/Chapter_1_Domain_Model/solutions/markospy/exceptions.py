class DomainError(Exception):
    pass


class NoAvailableVet(DomainError):
    def __init__(self):
        self.message = "No available vet"
        super().__init__(self.message)
