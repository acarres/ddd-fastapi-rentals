from shared.domain.errors.domain_error import DomainError

class BookingNotActive(DomainError):
    """Booking is not active."""
    pass