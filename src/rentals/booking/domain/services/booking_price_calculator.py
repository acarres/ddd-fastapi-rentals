from typing import Self
from shared.domain.value_objects.date_range import DateRange
from rentals.booking.domain.errors.invalid_nightly_rate import InvalidNightlyRate


class BookingPriceCalculator:
    DISCOUNT_THRESHOLD_DAYS = 7
    DISCOUNT_PERCENT = 10

    @staticmethod
    def calculate_total_cents(date_range: DateRange, nightly_rate_cents: int) -> int:
        if nightly_rate_cents <= 0:
            raise InvalidNightlyRate()

        days = date_range.days()
        total = days * nightly_rate_cents

        if days >= BookingPriceCalculator.DISCOUNT_THRESHOLD_DAYS:
            discount = (total * BookingPriceCalculator.DISCOUNT_PERCENT) // 100
            total = total - discount

        return total