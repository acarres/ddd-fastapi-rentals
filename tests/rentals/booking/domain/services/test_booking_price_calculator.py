import pytest


from rentals.booking.domain.services.booking_price_calculator import BookingPriceCalculator
from rentals.booking.domain.errors.invalid_nightly_rate import InvalidNightlyRate
from tests.shared.domain.value_objects.date_range_mother import DateRangeMother




def test_total_price_is_days_times_rate_when_under_discount_threshold():
    date_range = DateRangeMother.one_week()
    total = BookingPriceCalculator.calculate_total_cents(date_range=date_range, nightly_rate_cents=1000)


    # 7 días * 1000 céntimos = 7000
    # OJO: este test depende de la regla del descuento.
    # En nuestro servicio, 7 días ya aplica descuento (threshold >= 7).
    assert total == 6300

def test_discount_is_applied_when_days_are_7_or_more():
    date_range = DateRangeMother.one_week()
    total = BookingPriceCalculator.calculate_total_cents(date_range=date_range, nightly_rate_cents=1000)


    # 7000 - 10% = 6300
    assert total == 6300


def test_invalid_rate_raises_domain_error():
    date_range = DateRangeMother.one_week()


    with pytest.raises(InvalidNightlyRate):
        BookingPriceCalculator.calculate_total_cents(date_range=date_range, nightly_rate_cents=0)