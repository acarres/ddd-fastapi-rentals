from dataclasses import dataclass
from datetime import date

from shared.domain.errors.date_range_exception import InvalidDateRange


@dataclass(frozen=True)
class DateRange:
    start: date
    end: date

    def __post_init__(self) -> None:
        if self.end <= self.start:
            raise InvalidDateRange("End date must be after start date")
    
    def contains(self, value: date) -> bool:
        return self.start <= value <= self.end