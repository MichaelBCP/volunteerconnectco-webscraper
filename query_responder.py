from google import genai
from dotenv import load_dotenv
import os

def answer_query(query, full_text):
    load_dotenv()
    gemini_api_key = os.getenv('GEMINI_API_KEY')

    client = genai.Client(api_key=gemini_api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=query + full_text
    )

    return response.text

if __name__ == '__main__':
    print(answer_query('favorite drink', 'you like orange juice'))