from shared.domain.errors.domain_error import DomainError


class InvalidBookingStatus(DomainError):
    """Invalid booking status value."""

    def __init__(self, value: str):
        self.value = value
        super().__init__(f"Invalid booking status: {value}")

