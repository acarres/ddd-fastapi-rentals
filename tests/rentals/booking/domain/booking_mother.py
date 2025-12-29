from rentals.booking.domain.booking import Booking
from tests.shared.domain.value_objects.date_range_mother import DateRangeMother
from uuid import uuid4


class BookingMother:
    @staticmethod
    def active() -> Booking:
        return Booking.create(id=uuid4(), date_range=DateRangeMother.january_2025())