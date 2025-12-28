from enum import Enum

from rentals.booking.domain.errors.invalid_booking_status import InvalidBookingStatus


class BookingStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    ACTIVE = "active"

    @classmethod
    def _missing_(cls, value: object) -> "BookingStatus":
        raise InvalidBookingStatus(str(value))

    def equals(self, other: "BookingStatus") -> bool:
        return self.value == other.value