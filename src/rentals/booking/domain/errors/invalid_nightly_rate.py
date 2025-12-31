from shared.domain.errors.domain_error import DomainError


class InvalidNightlyRate(DomainError):
    """Se lanza cuando el precio por día no es válido."""
    pass