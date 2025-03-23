import os
import random
from groq import Groq
import json
import random 
def getResponseFormGroq(prompt):
    client = Groq(
        api_key=random.choice(json.loads(os.getenv('groqAPI'))),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=1.3,
        model="deepseek-r1-distill-llama-70b",
        seed=random.randint(1,111111119786),
    )
    return chat_completion.choices[0].message.content






def groqimage(imageURL):
    client = Groq(api_key=random.choice(json.loads(os.getenv('groqAPI'))),)
    completion = client.chat.completions.create(
        model="llama-3.2-90b-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe this image. Describe precisely what you can see here yet keeping the explanition not so long. and return as a text that other ai models can understand the exact image. Describe al least 50 words under 150 words. Return just the explanition without anything. Explain in one paragraph"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": imageURL
                        }
                    }
                ]
            },

        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        stop=None, 
    )

    return completion.choices[0].message.content


def getCommentForPost(caption, image="no", imageExpl = ""):
        
        with open("./main/ai/personality.json") as personalitys:
            personalityes = json.load(personalitys)
        
        personality1 = random.choice(personalityes)
        personality2 = random.choice(personalityes)
        if image == "no":
            prompt = '''Write 2 comment for a post where the caption is {' '''+caption+''' ' } and the commenter personalites are {'''+personality1+" and " +personality2+'''}. Try to mimic real person and keep them short and on the point. give output in json form. Just the comment is needed without any other data point. Here is example output, ["comment one","comment two"]. Dont forgot to check the syntex again.'''
            
        else:
            prompt = '''Write 2 comment for a post where the caption is { ' '''+caption+''' ' } This Post containt a image that describe to, {' '''+imageExpl+'''  '}.and the commenter personalites are {'''+personality1+" and " +personality2+'''}. Try to mimic real person and keep them short and on the point. give output in json form. Just the comment is needed without any other data point. Here is example output, ["comment one","comment two"]. Dont forgot to check the syntex again.'''
        response = getResponseFormGroq(prompt)
        usefulltext = response.split("</think>")[1]
        if "```json" in usefulltext:
            usefulltext = usefulltext.replace("```json","")
            usefulltext = usefulltext.replace("```","")

        usefulltext = usefulltext.replace("\n","")
        comments = json.loads(usefulltext)
        return comments


def getPost():
    with open("./main/ai/postpersonalit.json") as personalitys:
            personalityes = json.load(personalitys)
    personality1 = random.choice(personalityes)
    additionalPersonality = ["gen z","normal"]
    responce =  getResponseFormGroq("Write a short tweet like and on the point post  in social media with personally of { "+personality1+" and he is a "+random.choice(additionalPersonality)+" }. Write the post in plain text without any quotation or any other format.")
    responce = responce.split("</think>")[1]
    responce = responce.replace("\n","")
    return responce


