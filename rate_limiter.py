import time
import datetime

class TimeOperator:
    def __init__(self):
        self.query_times = []
        # Query times are TimeSignature objects (time.time(), datetime.date.today())
        self.requests_per_minute_limit = 10
        self.requests_per_day_limit = 15

        self.load_time_signatures()

    def load_time_signatures(self):
        query_times = []

        with open("time_signature_logs.txt", "r") as logs:
            for line in logs:
                query_time = line.strip().split("|")
                query_times.append(query_time)

        self.query_times = query_times

    def requests_this_minute(self):
        current_time = time.time()
        minute_requests = 0

        for query_time in self.query_times:
            if current_time - query_time.epoch_time < 60:
                minute_requests += 1

        return minute_requests

    def requests_this_day(self):
        current_date = datetime.date.today()
        day_requests = 0

        for query_time in self.query_times:
            if query_time.date_time == current_date:
                day_requests += 1

        return day_requests

    def is_time_authorized(self):
        for time_signature in self.query_times:
            if isinstance(time_signature, TimeSignature):
                try:
                    x = time_signature.epoch_time
                    y = time_signature.date_time
                except Exception as e:
                    self.query_times.remove(time_signature)
            else:
                print("Invalid Signature")
                self.query_times.remove(time_signature)

        if self.requests_this_minute() >= self.requests_per_minute_limit:
            print("Exceeded requests per minute")
            return False

        if self.requests_this_day() >= self.requests_per_day_limit:
            print("Exceeded requests per day")
            return False

        print("Within requests limit (hopefully)")
        return True

    def add_query_time(self, time_signature):
        self.query_times.append(time_signature)


class TimeSignature:
    def __init__(self):
        self.epoch_time = time.time()
        self.date_time = datetime.date.today()
        self.log_time_signature()

    def to_string(self):
        return str(self.epoch_time) + "|" + str(self.date_time)

    def log_time_signature(self):
        with open("time_signature_logs.txt", "a") as logs:
            logs.write(self.to_string() + "\n")