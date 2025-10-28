import pyperclip
from scraping_tools import*
from query_responder import*

url = str(input("what url: "))
full_text = get_text_from_url(url)
print("this is the text:"+full_text)
print("got_text")

row = [
    answer_query("\n" + "js tell me Name of Organization (DONT ABBREVIATE), WRITE NOTHING ELSE", full_text),
    answer_query(
        "what's the volunteer opportunity title for example Volunteer at Berkeley Art Center, only write the volunteer title nothing else", full_text),
    url,
    get_img_from_url(url),
    answer_query(
        "\n" + "position date (ie on calendar ie March 25-29, put ongoing if not clear, ONLY ANSWER THE QUESTION WRITE NOTHING ELSE", full_text),
    answer_query(
        "pls summarise in 5 well written sentences for potential volunteers as a description, an example for a different organization would be Abrahamic Alliance International is a charitable non-profit organization uniting Jews, Christians, and Muslims for active peacebuilding and poverty relief. AAi began with a simple dream that compassionate collaboration between Jews, Christians, and Muslims can build lasting bridges of understanding and respect between our communities. By uniting to serve the poor in obedience to divine commands, our grassroots movement is showing the world that peaceful coexistence between Jews, Christians, and Muslims is not a naive and distant dream, but a growing and present reality here and now.", full_text),
    answer_query(
        "age requirement, if none, say None--do not put nothing Always put a + after whatever number if necessary Examples: 15+ 12+13-18, ONLY ANSWER ACCORDING TO EXAMPLE NO EXTRA TEXT", full_text),
    answer_query(
        "\n" + "skill requirements, put None if there's none but never leave blank Possible skill requirements: Experienced with Adobe Design, Familiar Working with Children, etc. ONLY ANSWER ACCORDING TO EXAMPLE NO EXTRA TEXT", full_text),
    answer_query("If its in-person ANSWER THE ADDRESS AND NOTHING ELSE IF U CANNOT find the adress put N/A otherwise write 'virtual' AND NOTHING ELSE thx", full_text),
    answer_query(
        "Which of these passion areas does it fit best? BE VERY GENEROUS MORE IS BETTER Government Arts and Culture Faith-Based Economic Animal Welfare Community Building Youth Services Environmental" + "\n" + "To answer write the multiple that u think fit comma seperated ie 'Government, Community Building, Youth Services' WRITE NOTHING ELSE", full_text),
    answer_query(
        "Which of these specific skills does it fit best? BE VERY GENEROUS MORE IS BETTER Business Management, Canvassing/Campaigning, Communications, Computers and IT, Customer Service, Elderly, Health and Medicine, Homelessness, Language, Leadership, Legal/Advocacy, LGBTQ+, Life Sciences, Mental Health, Music, Performing Arts, Public Speaking, Sports and Recreation, STEM, Tutoring, Visual Arts" + "\n" + "To answer write the multiple that u think fit comma seperated ie 'Communications, Customer Service, Life Sciences, Health and Medicine, Public Speaking' WRITE NOTHING ELSE", full_text),
    answer_query(
        "Include all of these filters unless it doesnt fit one of them, so unless for example it has a age limit both HS and MS would apply High School, In-Person, Middle School, Virtual" + "\n" + "To answer write the multiple that u think fit comma seperated ie 'High School, In-Person, Virtual' WRITE NOTHING ELSE", full_text),
]

def clean(t):
    return t.replace('\n', ' ').replace('\r', ' ').strip()

for i in range(len(row)):
    row[i] = clean(row[i])

tsv_row = "\t".join(row)

pyperclip.copy(tsv_row)

print("row copied to clipboard")