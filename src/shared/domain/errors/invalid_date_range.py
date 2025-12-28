from shared.domain.errors.domain_error import DomainError


class InvalidDateRange(DomainError):
    """Exception raised when a date range is invalid."""
    pass