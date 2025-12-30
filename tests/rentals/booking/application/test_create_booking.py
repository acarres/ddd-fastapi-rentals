import pytest
from datetime import date
from uuid import UUID

from rentals.booking.application.create_booking import CreateBooking
from rentals.booking.application.create_booking_request import CreateBookingRequest


def test_create_booking_returns_an_id():
    use_case = CreateBooking()
    booking_id = use_case.execute(CreateBookingRequest(start_date=date(2025, 1, 1), end_date=date(2025, 1, 31)))
    assert isinstance(booking_id, UUID)