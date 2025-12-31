from google import genai
import time

# Directly hardcode the key
GEMINI_API_KEY = "micheal dm me for this"

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
