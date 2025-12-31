from datetime import date
from shared.domain.value_objects.date_range import DateRange


class DateRangeMother:
    @staticmethod
    def january_2025() -> DateRange:
        return DateRange(start=date(2025, 1, 1), end=date(2025, 1, 31))

    @staticmethod
    def one_week() -> DateRange:
        return DateRange(start=date(2025, 1, 1), end=date(2025, 1, 7))

    @staticmethod
    def invalid() -> DateRange:
        return DateRange(start=date(2025, 1, 31), end=date(2025, 1, 1))

