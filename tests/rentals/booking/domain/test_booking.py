import pytest
from datetime import date
from uuid import uuid4
from rentals.booking.domain.booking import Booking
from rentals.booking.domain.booking_status import BookingStatus
from rentals.booking.domain.errors.booking_not_active import BookingNotActive
from shared.domain.value_objects.date_range import DateRange
from tests.rentals.booking.domain.booking_mother import BookingMother


def test_booking_is_created_when_dates_are_valid():
        booking = BookingMother.active()

        assert booking.id is not None
        assert booking.date_range is not None
        assert booking.status.equals(BookingStatus.ACTIVE)

def test_booking_status_is_not_a_free_string():
        booking = BookingMother.active()
        assert isinstance(booking.status, BookingStatus)

def test_booking_can_be_cancelled_when_active():
    booking = BookingMother.active()
    booking.cancel()

    assert booking.status.equals(BookingStatus.CANCELLED)


def test_booking_cannot_be_cancelled_when_not_active():
    booking = BookingMother.active()
    booking.cancel()

    with pytest.raises(BookingNotActive):
        booking.cancel()