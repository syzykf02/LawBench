'''
Usage:
Ark v3 sdk
pip install volcengine-python-sdk
'''

from dotenv import load_dotenv
from volcenginesdkarkruntime import Ark

load_dotenv('../.env')

# follow this document (https://www.volcengine.com/docs/82379/1263279) to generate API Key
# put API Key into environment variable ARK_API_KEY or specify api_key directly in Ark()
# api_key = os.environ['ARK_API_KEY']
api_key = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcmstY29uc29sZSIsImV4cCI6MTcxNjQzNDkwMSwiaWF0IjoxNzE2MTM0OTAxLCJ0IjoidXNlciIsImt2IjoxLCJhaWQiOiIyMTAwOTYzMDQ2IiwidWlkIjoiMCIsImlzX291dGVyX3VzZXIiOnRydWUsInJlc291cmNlX3R5cGUiOiJlbmRwb2ludCIsInJlc291cmNlX2lkcyI6WyJlcC0yMDI0MDUxOTE1MjgyMi0yamZoZCJdfQ.huFYLtyqbMrvRfCbk5A0KjCOig5sD0voqjHeg2_k0yNDu_7Dhtej9hcP7Dy2DZIQk9NrrU4nTsFHzum9jaITU3FNdTRrgM_I6uM5WDkOGL4U3Ib4Putfjb4R-WE46XfG_kVbzlFS4WzwVOpgv8U6k0-jBMZPmraOskbCGz-wlA5RO4cwIxFysfaTmcUS1FlSjjC28pdIL7ZgOy9T3KfNIHEuYH7WkRa8rPalp7fF_5ftM4yOhPpJnv4Jj9TkLJ9hnizJU9EXEIWJ5NgjZxxnrgj2qpyampkhiZegCThZlpOrApHBji7tjrqstkx_2o7WlEN-Pl4ttXQCmeN0xgplKw"
client = Ark(api_key=api_key)


def chat(query: str):
    # Non-streaming:
    print("----- standard request -----")
    completion = client.chat.completions.create(
        model="ep-20240519152822-2jfhd",
        messages=[
            {
                "role": "user",
                "content": query,
            },
        ],
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content


def chat_stream(query):
    # Streaming:
    print("----- streaming request -----")
    stream = client.chat.completions.create(
        model="ep-20240519152822-2jfhd",
        messages=[
            {
                "role": "user",
                "content": query,
            },
        ],
        stream=True,
    )
    for chunk in stream:
        if not chunk.choices:
            continue

        print(chunk.choices[0].delta.content, end="")
    print()


if __name__ == "__main__":
    chat('公司要求员工加班是否可以拒绝？')
    # chat_stream('公司要求员工加班是否可以拒绝？')
