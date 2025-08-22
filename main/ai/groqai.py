import os
import random
from groq import Groq
import json
import random 
from dotenv import load_dotenv

load_dotenv()
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
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
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


def getCommentForPost(caption,context, image="no", imageExpl = ""):
        
        with open("./main/ai/personality.json") as personalitys:
            personalityes = json.load(personalitys)
        
        personality1 = random.choice(personalityes)
        personality2 = random.choice(personalityes)
        if image == "no":
            prompt = '''Write 2 comment for a post where the caption is {' '''+caption+''' ' } and the commenter personalites are {'''+personality1+" and " +personality2+'''}.  Use other people post as context, here is some data of what other people are saying '''+context+'''. Use this data only as context, never rewrite the same exprasiton, try to come up with something different using the context and the idia of user data.. give output in json form. Just the comment is needed without any other data point. Here is example output, ["comment one","comment two"]. Dont forgot to check the syntex again.'''
            
        else:
            prompt = '''Write 2 comment for a post where the caption is { ' '''+caption+''' ' } This Post containt a image that describe to, {' '''+imageExpl+'''  '}.and the commenter personalites are {'''+personality1+" and " +personality2+'''}.  Use other people post as context, here is some data of what other people are saying '''+context+'''. Use this data only as context, never rewrite the same exprasiton, try to come up with something different using the context and the idia of user data. give output in json form. Just the comment is needed without any other data point. Here is example output, ["comment one","comment two"]. Dont forgot to check the syntex again.'''
        response = getResponseFormGroq(prompt)
        usefulltext = response.split("</think>")[1]
        if "```json" in usefulltext:
            usefulltext = usefulltext.replace("```json","")
            usefulltext = usefulltext.replace("```","")

        usefulltext = usefulltext.replace("\n","")
        comments = json.loads(usefulltext)
        return comments


def getPost(context):
    with open("./main/ai/postpersonalit.json") as personalitys:
            personalityes = json.load(personalitys)
    personality1 = random.choice(personalityes)
    additionalPersonality = ["gen z","normal"]
    # responce =  getResponseFormGroq("Write a short tweet like and on the point post  in social media with personally of { "+personality1+" and he is a "+random.choice(additionalPersonality)+" }. Use other people post as context, here is some data of what other people are saying "+context+". Use this data only as context, never rewrite the same exprasiton, try to come up with something different using the context and the idea of user data. Use these data as inpreation and dont answer them . Write the post in plain text without any quotation or any other format. Make the post short and small like really short.")
    responce = getResponseFormGroq("You are a creative social media content generator your personality is "+personality1+" and "+random.choice(additionalPersonality)+". I will provide you with a few example posts that share a common theme or topic. Your task is to analyze the underlying idea of these posts and then generate an entirely new post that reflects the same theme, but without using the exact wording or keywords found in the examples. Ensure that the generated post is creative, unique, and in line with the context provided. Also, make the post size approximately the average length of recent posts. The given post will be in [] under a parent {}. every [] means one post. Here is some recent post, "+context+" , generate a new post with these data. The post only would be in plain text without anything, just the post.")
    responce = responce.split("</think>")[1]
    responce = responce.replace("\n","") 
    return responce

 