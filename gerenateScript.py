from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
client = OpenAI()

contents = open('contents.txt').read()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content" : "You are a writer for creating video content."},
        {"role": "user", "content": f"Generate a script for a video, no longer than 45 seconds, summarizing the key contents of the following document summary. Should NOT have any stage cues -- just text. Generate a title as well {contents}"}
    ]
)

# print(response)
with open('script.txt', 'w') as f:
    f.write(response.choices[0].message.content)