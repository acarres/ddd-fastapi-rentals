from datetime import date


class CreateBookingRequest:
    def __init__(self, start_date: date, end_date: date):
        self.start_date = start_date
        self.end_date = end_date