import os
from openai import OpenAI, AzureOpenAI

def testAzureOpenAI(messages):
    client = AzureOpenAI(
        api_key = os.getenv("AZURE_OPENAI_API_KEY"),
        api_version = "2024-02-01",
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    response = client.chat.completions.create(
        model="gpt-35-turbo-16k",
        messages=messages
    )
    return response.choices[0].message.content

def testOpenAI(messages):
    client = OpenAI(
        api_key = os.getenv("OPENAI_API_KEY")
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content

messages1 = [
    {
        "role": "system",
        "content": "answer the question using only the following information: "
            "there are no kangaroos in Australia."
    },
    {
        "role": "user",
        "content": "are there kangaroos in Australia?"
    }
]

messages2 = [
    {
        "role": "user",
        "content": "are there kangaroos in Australia?"
    }
]

messages3 = [
    {
        "role": "user",
        "content": "answer the question: are there kangaroos in Australia? "
            "using only the following information: "
            "there are no kangaroos in Australia."
    }
]

print("question: are there kangaroos in Australia?\n")
print("OpenAI with sys msg:                  %s\n" % testOpenAI(messages1))
print("OpenAI no sys msg, no context:        %s\n" % testOpenAI(messages2))
print("OpenAI no sys msg, with context:      %s\n" % testOpenAI(messages3))
print("AzureOpenAI with sys msg:             %s\n" % testAzureOpenAI(messages1))
print("AzureOpenAI no sys msg, no context:   %s\n" % testAzureOpenAI(messages2))
print("AzureOpenAI no sys msg, with context: %s\n" % testAzureOpenAI(messages3))
