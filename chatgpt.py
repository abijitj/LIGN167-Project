import os
from dotenv import load_dotenv
import openai
from openai import OpenAI
from typing import Optional
# Load environment variables from a .env file
load_dotenv()

# Get the OpenAI API key from the environment variable
openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key:
    print("OpenAI API key loaded successfully.")
else:
    print("Failed to load OpenAI API key.")

client = OpenAI(
    api_key=openai_api_key,  # This is the default and can be omitted
)


def get_chatgpt_response(prompt: str)->Optional[str]:
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4o-mini",
    )
    # Print the response from the ChatGPT API
    return response.choices[0].message.content

print(get_chatgpt_response("Whats 5+5"))