import pytest
from datetime import date
from shared.domain.value_objects.date_range import DateRange
from shared.domain.errors.invalid_date_range import InvalidDateRange
from tests.shared.domain.value_objects.date_range_mother import DateRangeMother


def test_valid_date_range_is_created():
    date_range = DateRangeMother.january_2025()

    assert date_range.contains(date_range.start)


def test_invalid_date_range_raises_error():
    with pytest.raises(InvalidDateRange):
        DateRangeMother.invalid()