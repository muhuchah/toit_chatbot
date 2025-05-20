from openai import OpenAI
import jsonlines
import time
import os

# Openai Variables
API_KEY = os.environ["API_KEY"]
BASE_URL = os.environ["BASE_URL"]

def openai_response(usermessage, sys_prompt, data):
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    if "{data}" in sys_prompt:
        content = sys_prompt.format(data=data)
    else:
        content = sys_prompt

    usermessage += "\nSTRICTLY Do not give me any information about anything that is not mentioned in the PROVIDED CONTEXT."

    ex = True
    while ex:
        ex = False 
        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": content},
                    {"role": "user", "content": usermessage}
                ]
            )
        except:
            time.sleep(1)
            ex = True

    return completion.choices[0].message.content


def openai_generate_title(user_message):
    # Handle Prompt
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    ex = True
    while ex:
        ex = False 
        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a chatbot, skilled in answering user's questions, generate a good and small (under 16 characters) title for the user message"},
                    {"role": "user", "content": user_message}
                ]
            )
        except:
            time.sleep(1)
            ex = True
   
    return completion.choices[0].message.content


def create_embedding(data):
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    i = 0
    ex = True
    while ex:
        ex = False 
        try:
            response = client.embeddings.create(
                input = data,
                model = 'text-embedding-ada-002',
                encoding_format = 'float'
            )
        except:
            print(i)
            i += 1
            time.sleep(5)
            ex = True

    return response.data[0].embedding


def read_jsonl_file(file_path):
    data = []
    with jsonlines.open(file_path) as reader:
        for line in reader.iter():
            data.append(line)
    return data
