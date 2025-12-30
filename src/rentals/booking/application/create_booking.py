from datetime import date
from uuid import UUID

from rentals.booking.domain.booking import Booking
from shared.domain.value_objects.date_range import DateRange
from rentals.booking.application.create_booking_request import CreateBookingRequest


class CreateBooking:
    def execute(self, request: CreateBookingRequest) -> UUID:
        date_range = DateRange(request.start_date, request.end_date)

        booking = Booking.create(date_range)

        return booking.id