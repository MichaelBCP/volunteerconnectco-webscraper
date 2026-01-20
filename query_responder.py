from google import genai
from dotenv import load_dotenv
import os
import time
import datetime
from pydantic import BaseModel, Field

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

    def answer_json_query(self, queries, field_texts, full_text):
        class InfoBlock(BaseModel):
            opportunity_title: str = Field(description="Opportunity title, Make the title as informative as possible but don't keep it too long. You can make up/modify the title as you see fit -- whatever gives people the best info on this opportunity and what it entails")
            name_of_organization: str = Field(description="Organization name, Put the name in its simplest form. Don't abbreviate. San Jose Parks, Friends of Children with Special Needs, Martin Luther King Library")
            description: str = Field(description="Description should be a short paragraph. 3-5 sentences is fine. Add a short 1-2 sentence one if there is no description on the website, but try to find one. Make it as informative as possible. Focus on what this opportunity is doing and what the volunteer will get out of it.")
            locations: str = Field(description="If it's in person, put the full address. If it's virtual, put virtual. If it's hybrid, put the address and say that it's sometimes virtual.")
            when_in_day: str = Field(description="Time of day the opportunity is at")
            position_date_start_end: str = Field(description="Date of opportunity, put ongoing if no specific dates, NEVER leave blank!")
            age_requirement: str = Field(description="Age requirement, if none, say 'none'--do not put nothing, Always put a + after whatever number if necessary Examples: 15+, 12+, 13-18")
            experience_needed: str = Field(description="Experience needed, same with age, put none if there's none but never leave blank, Possible skill requirements: Experienced with Adobe Design, Familiar Working with Children, etc.")
            passion_areas: str = Field(description="Passion Areas, for example 'Community Building, Youth Services'")
            specific_skills: str = Field(description="Specific skills needed")
            middle_school_high_school: str = Field(description="For high schoolers, middle schoolers, or both")

        if self.time_op.is_time_authorized():
            new_query = self.Query(self.client, queries, full_text)
            self.time_op.add_query_time(new_query.time_signature)


    class Query:
        def __init__(self, gemini_client, query, full_text, model="gemini-3-flash-preview"):
            self.query = query
            self.full_text = full_text
            self.gemini_client = gemini_client
            self.time_signature = TimeSignature()
            self.model = model

        def query_response(self):
            response = self.gemini_client.models.generate_content(
                model=self.model,
                contents=self.query + "\n" + self.full_text
            )
            print("✅ Query answered")
            return response

        #def json_query_response(self, field_texts):

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