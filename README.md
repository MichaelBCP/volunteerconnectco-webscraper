# volunteerconnectco-webscraper
Webscraper for Volunteer Connect

This tool is used to generate a row of information using Google Gemini LLM to process info extracted using BeautifulSoup4 from the url provided. It is currently configured to VolunteerConnect's specific information needs.

Volunteer Connect Website: https://www.volunteerconnectco.org/


**Requirements**
The following packages need to be installed:
- CSV
- Pydantic
- OS
- google genai
- bs4 BeautifulSoup
- urllib.parse

User will also need a valid GEMINI_API_KEY environmental variable
