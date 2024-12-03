import os
from dotenv import load_dotenv
import openai
from openai import OpenAI
from typing import List, Optional
import re


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

with open('raw_transcript.txt', 'r') as file:
    transcript_text = file.read()
print(len(transcript_text), len(transcript_text.split(' ')))

def get_summary(transcript_text: str)-> str:
    summary_prompt = f"""You are a text summarizer that takes in college lectures and summarizes them.
You only refer to content included within the lecture transcript, and do not generate anything that isn't already present.
Your task is to create a 1 paragraph summary of the following lecture transcript.
Don't refer to things that are external to the content such as the professor talking about people coming to class late.
Do include things that are important to students like references to homework and exams.
The vast majority of the summary should be about the content of the lecture. It should follow the same order as the lecture and include the most important points.
Do not include any extra description, just give your summary.
Lecture Transcript:
{transcript_text}
"""
    return get_chatgpt_response(summary_prompt)

def get_stamped_topics(transcript_text: str)->List[List[str|int]]:
    list_of_topics_prompt = f"""You are a text summarizer that takes in college lecture transcripts and creates topic lists from them.
You will create a list of topics in this format:
- Topic 1 here
- Topic 2 here

Here's an example in the context of climate change:
- Causes of Climate Change
- Impact on Ecosystems
- Human Health Effects
- Mitigation Strategies
- Policy and Regulation
- Renewable Energy Solutions
- Climate Change Adaptation

Each topic should be a single sentence that doesn't end with a period. It should be a high-level overview of the topic.
Don't refer to things that are external to the content such as the professor talking about people coming to class late. This is important.
Do include things that are important to students like references to homework and exams.
The topic list should be in the same order as the lecture transcript and be fairly comprehensive. Include all the major topics and important points.
For an hour-long lecture, you should have around 10 topics.

Your output should only be the topic list in the given format, nothing else.

Here is the transcript:
{transcript_text}
"""

    numbered_text = transcript_text[:]
    min_length_between_numbers = 150
    current_length = 0
    current_num = 1
    for char in transcript_text:
        numbered_text += char
        if char == ' ' and current_length >= min_length_between_numbers:
            numbered_text += '{!' + str(current_num) + '!}'
            current_length = 0
            current_num += 1
        current_length += 1

    number_stamp_example = "{!number!}"
    number_stamp_example_2 = "{!2!}"
    lecture_topics = get_chatgpt_response(list_of_topics_prompt)

    topics_organizer_prompt = f"""You are a text organizer that takes in college lecture transcripts and a topic list to find where each topic starts and ends.

The topic list is in this format:
- Topic 1 here
- Topic 2 here

The transcript is numbered in a special way with number stamps. Each number stamp is in the form of "{number_stamp_example}". 
Here's an example: "{number_stamp_example_2}".

Your task is to organize the transcript into sections based on the topics by determining the start and end of each topic based on number stamps.
The topics in the transcript will be in the same order as the topic list.

You will output the list of topics with the corresponding number of the number stamp that starts closest to the beginning of the topic but is before the beginning of the timestamp as well as the
closest timestamp after it that follows the end of the topic.

If the end of a topic is the very end of the transcript put -1. This should only happen for the last topic. This may not always happen for the last topic if it is clearly
concluded in the transcript.

Here's an example where you're given a full transcript and this list of topics:
- Causes of Climate Change
- Impact on Ecosystems
- Human Health Effects
- Mitigation Strategies
- Policy and Regulation

Your output is the list of topics with the corresponding number stamps:
- Causes of Climate Change | 1 | 15
- Impact on Ecosystems | 18 | 45
- Human Health Effects | 42 | 67
- Mitigation Strategies | 123 | 150
- Policy and Regulation | 145 | -1

Your output should only be the list of topics with the corresponding number stamp, nothing else.

Here is the list of topics:
{lecture_topics}
Here is the transcript with number stamps:
{numbered_text}

Once again, make sure that your output rigidly follows the specified format. The end number stamps should always be after the start number stamps.
Make sure to follow the format from the previous example.

"""

    #summary = get_chatgpt_response(summary_prompt)
    #print(numbered_text)
    #lecture_topics = get_chatgpt_response(list_of_topics_prompt)
    topic_stamps = get_chatgpt_response(topics_organizer_prompt)
    full_topics = [] # List of lists of the form [topic, start_number, end_number, topic content]
    for topic_stamp in topic_stamps.split('\n'):
        #print(topic_stamp)
        processed_topic_stamp = topic_stamp[topic_stamp.find('-') + 1:].strip().split('|')
        topic = processed_topic_stamp[0].strip()
        print(processed_topic_stamp)
        start_number = processed_topic_stamp[1].strip()
        end_number = processed_topic_stamp[2].strip()
        full_topics.append([topic, start_number, end_number])


    for i in range(len(full_topics)):
        start_number = full_topics[i][1]
        end_number = full_topics[i][2]
        relevant_text = numbered_text.split('{!' + str(start_number) + '!}')[1]
        if end_number != -1:
            relevant_text = relevant_text.split('{!' + str(end_number) + '!}')[0]
        
        number_stamp_pattern = r"\{\!\d+\!\}"
        relevant_text = re.sub(number_stamp_pattern, "", relevant_text)
        full_topics[i].append(relevant_text)
    return full_topics


def get_bullet_points(topic: str, content: str)->str:
    bullet_points_prompt = f"""You are a text summarizer that takes in college lecture transcripts and creates bullet points from them. In this case, you have a topic as well as the content of the topic from a lecture.
You will output a list of informative and concise bullet points on that topic based on the lecture material. Do not deviate from the content of the lecture or make anything up.
Each bullet point should not end with a period
Here is an example of what you should output:
- Bullet point 1 here
- Bullet point 2 here

Your output should only be the bullet points in the given format, nothing else."""
    print(topic)
    bullets = get_chatgpt_response(bullet_points_prompt + f"\nTopic: {topic}\nContent: {content}")
    print(bullets)
    print('\n')
    return bullets

print(get_summary(transcript_text))
stamped_topics = get_stamped_topics(transcript_text)
bullet_points = []
for topic in stamped_topics:
    bullet_points.append((topic[0], get_bullet_points(topic[0], topic[3])))

print(bullet_points)