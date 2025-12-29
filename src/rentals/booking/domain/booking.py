from dataclasses import dataclass
from uuid import UUID, uuid4

from rentals.booking.domain.errors.booking_not_active import BookingNotActive
from shared.domain.value_objects.date_range import DateRange

from rentals.booking.domain.booking_status import BookingStatus

@dataclass
class Booking:
    id: UUID
    date_range: DateRange
    status: BookingStatus

    @staticmethod
    def create(date_range: DateRange) -> "Booking":
        return Booking(id=uuid4(), date_range=date_range, status=BookingStatus.ACTIVE)

    def cancel(self) -> None:
        if self.status != BookingStatus.ACTIVE:
            raise BookingNotActive()
        self.status = BookingStatus.CANCELLED