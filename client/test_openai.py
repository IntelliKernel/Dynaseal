from openai import OpenAI


client = OpenAI(
    api_key="asdfghjkl",
    base_url="http://127.0.0.1:8000/api/v1",
)

# # not stream
# response = client.chat.completions.create(
#     model="deepseek-chat",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Who are you?"},
#     ],
#     max_tokens=100,
#     temperature=0.6,
#     top_p=0.9,
#     stream=False,
# )
# print(response.choices[0].message.content)

# stream
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "user", "content": "请给我讲一个故事"},
    ],
    max_tokens=100,
    temperature=0.6,
    top_p=0.9,
    stream=True,
)
for message in response:
    print(message.choices[0].delta.content, end="", flush=True)
