import pytest
from datetime import date
from uuid import uuid4
from rentals.booking.domain.booking import Booking
from rentals.booking.domain.booking_status import BookingStatus
from rentals.booking.domain.errors.booking_not_active import BookingNotActive
from shared.domain.value_objects.date_range import DateRange


def test_booking_is_created_when_dates_are_valid():
        date_range = DateRange(start=date(2024, 1, 1), end=date(2024, 1, 10)) 
        booking = Booking.create(id=uuid4(), date_range=date_range)

        assert booking.id is not None
        assert booking.date_range == date_range
        assert booking.status.equals(BookingStatus.ACTIVE)

def test_booking_status_is_not_a_free_string():
        date_range = DateRange(start=date(2025, 1, 1), end=date(2025, 1, 31))
        booking = Booking.create(id=uuid4(), date_range=date_range)

        assert isinstance(booking.status, BookingStatus)

def test_booking_can_be_cancelled_when_active():
    date_range = DateRange(start=date(2025, 1, 1), end=date(2025, 1, 31))
    booking = Booking.create(id=uuid4(), date_range=date_range)
    booking.cancel()

    assert booking.status.equals(BookingStatus.CANCELLED)


def test_booking_cannot_be_cancelled_when_not_active():
    date_range = DateRange(start=date(2025, 1, 1), end=date(2025, 1, 31))
    booking = Booking.create(id=uuid4(), date_range=date_range)
    booking.cancel()

    with pytest.raises(BookingNotActive):
        booking.cancel()