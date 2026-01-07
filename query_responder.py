from google import genai
from dotenv import load_dotenv
import os
import time
import datetime

# Directly hardcode the key
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Initialize the Gemini client once
client = genai.Client(api_key=GEMINI_API_KEY)

def answer_query(query, full_text):
    time.sleep(1)
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=query + "\n" + full_text
    )
    time.sleep(1)
    print("✅ Query answered")
    return response.text

class GeminiOperator:
    def __init__(self):
        self.apikey = os.getenv('GEMINI_API_KEY')
        self.time_op = GeminiOperator.TimeOperator()
        self.client = None
        self.client_setup()

    def client_setup(self):
        self.apikey = os.getenv('GEMINI_API_KEY')
        self.client = genai.Client(api_key=self.apikey)

    class Query:
        def __init__(self, query, full_text):
            self.query = query
            self.full_text = full_text

        class TimeSignature:
            def __init__(self):
                self.epoch_time = time.time()
                self.date_time = datetime.date.today()

    class TimeOperator:
        def __init__(self):
            self.query_times = []
            #Query times are in format (time.time(), datetime.date.today())
            self.requests_per_minute = 10
            self.requests_per_day = 20

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

        def time_authorized(self):
            pass

if __name__ == '__main__':
    print(answer_query('favorite drink', 'you like orange juice'))