from idlelib.query import Query

from google import genai
from dotenv import load_dotenv
import os
import time
import datetime

class GeminiOperator:
    def __init__(self):
        self.time_op = GeminiOperator.TimeOperator()
        self.client = None
        self.client_setup()
        self.query_queue = []

    def client_setup(self):
        self.client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

    def queue_query(self, query, full_text):
        queued_query = self.Query(self.client, query, full_text)
        self.query_queue.append(queued_query)

    def log_error(self, error):
        with open("error_log.txt", "a") as error_file:
            error_file.write(f"{error}\n")

    def answer_query(self, query, full_text, strip_data=True):
        if self.time_op.is_time_authorized():
            new_query = self.Query(self.client, query, full_text)
            self.time_op.add_query_time(new_query.time_signature)

            try:
                if strip_data:
                    return new_query.query_response().text

                else:
                    return new_query.query_response()

            except Exception as e:
                print(f"Exception: {e}")
                self.log_error(e)

        else:
            print("Not time authorized")
            return "Exception"

    def merged_query(self, queries, full_text):
        full_query_text = "Answer each question separately, separate your answers with a single | between answers"
        query_number = 0

        for question in queries:
            query_number += 1
            full_query_text += question

            if query_number != len(queries):
                full_query_text += "|\n"

        merged_answer = self.answer_query(full_query_text, full_text)

        answers = merged_answer.split(sep="|")

        if len(answers) == len(queries):
            return answers

        else:
            print("Merged incorrectly")
            return "Exception"

    class Query:
        def __init__(self, gemini_client, query, full_text, model="gemini-3-flash-preview"):
            self.query = query
            self.full_text = full_text
            self.gemini_client = gemini_client
            self.time_signature = self.TimeSignature
            self.model = model

        def query_response(self):
            response = self.gemini_client.models.generate_content(
                model=self.model,
                contents=self.query + "\n" + self.full_text
            )
            print("✅ Query answered")
            return response

    class TimeOperator:
        def __init__(self):
            self.query_times = []
            #Query times are TimeSignature objects (time.time(), datetime.date.today())
            self.requests_per_minute_limit = 10
            self.requests_per_day_limit = 20

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
                if time_signature is TimeSignature():
                    try:
                        x = time_signature.epoch_time
                        y = time_signature.date_time
                    except Exception as e:
                        self.query_times.remove(time_signature)
                else:
                    print("Invalid Signature")
                    self.query_times.remove(time_signature)


            if self.requests_this_minute() > self.requests_per_minute_limit:
                print("Exceeded requests per minute")
                return False

            if self.requests_this_day() > self.requests_per_day_limit:
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


if __name__ == '__main__':
    newOperator = GeminiOperator()
    #print(newOperator.answer_query('favorite drink', 'you like orange juice'))
    #merged_query = newOperator.merged_query(("where is this event", "what time is the event"), "The event is the Abcd garden volunteering at Golden park. There will be 20 people and it starts at 9:30")