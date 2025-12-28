import pytest
from datetime import date
from shared.domain.value_objects.date_range import DateRange
from shared.domain.errors.invalid_date_range import InvalidDateRange


def test_date_range_is_created_when_dates_are_valid():
    date_range = DateRange(start=date(2025, 1, 1), end=date(2025, 1, 31))

    assert date_range.start == date(2025, 1, 1)
    assert date_range.end == date(2025, 1, 31)

def test_date_range_raises_error_when_end_is_before_start():
    with pytest.raises(InvalidDateRange):
        DateRange(start=date(2024, 1, 10), end=date(2024, 1, 1))

def test_date_range_contains_date_inside_range():
    date_range = DateRange(start=date(2024, 1, 1), end=date(2024, 1, 10))

    assert date_range.contains(date(2024, 1, 5)) is True
    assert date_range.contains(date(2024, 1, 20)) is False