from datetime import date
from uuid import UUID

from rentals.booking.domain.booking import Booking
from shared.domain.value_objects.date_range import DateRange


class CreateBooking:
    def execute(self, start_date: date, end_date: date) -> UUID:
        date_range = DateRange(start_date, end_date)
        booking = Booking.create(date_range)

        return booking.id