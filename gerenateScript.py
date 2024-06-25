from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
client = OpenAI()

contents = open('contents.txt').read()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content" : "You are a script writer for creating video content."},
        {"role": "user", "content": f"Create a script of a news broadcast about the contents of the following document summary: {contents}"}
    ]
)

# print(response)
with open('script.txt', 'w') as f:
    f.write(response.choices[0].message.content)