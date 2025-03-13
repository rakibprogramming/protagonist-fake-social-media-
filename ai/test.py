import os

from groq import Groq

client = Groq(
    api_key="",
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": ''''Write 5 ranodm comment for a post with caption "✈" with a image which describe to [A person siting in a air plane seat. Wearting red shirt. a sunglass]''',
        }
    ],
    model="deepseek-r1-distill-llama-70b",
)

print(chat_completion.choices[0].message.content)