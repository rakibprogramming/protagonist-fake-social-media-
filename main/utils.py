import requests
import random
import string
from PIL import Image
import boto3
from botocore.exceptions import ClientError
import os
import time

def generate_fantasy_name():
    consonant_syllables = [
        "bel", "thor", "mor", "dra", "thar", "lor", "kan", "ver", "sal", "gar",
        "fen", "tik", "vyr", "syl", "mir", "del", "grim", "brin", "quar", "blar",
        "cor", "drak", "fyn", "geth", "harl", "jor", "kren", "morn", "nul",
        "pyr", "qor", "rhen", "sarn", "tul", "vorn", "welk", "xan", "yor", "zul"
    ]
    vowel_syllables = [
        "ar", "el", "essa", "en", "al", "ion", "eth", "wyn", "or", "ir", "ur",
        "ara", "elle", "indra", "ora", "ae", "ia", "elle", "ina", "ora", "uun",
        "aia", "eira", "oya", "ava", "ire", "olo", "umi"
    ]
    
    name_parts = []
    num_syllables = random.randint(2, 4) 

    if random.random() < 0.7:
        current_syllable = random.choice(consonant_syllables)
    else:
        current_syllable = random.choice(vowel_syllables)
    name_parts.append(current_syllable)

    for _ in range(num_syllables - 1):
        last_char = name_parts[-1][-1].lower()
        if last_char in 'aeiou':
            next_syllable = random.choice(consonant_syllables)
        else:
            next_syllable = random.choice(vowel_syllables)
        name_parts.append(next_syllable)
    
    return ''.join(name_parts).capitalize()

def nameGenerator():

    fullName = generate_fantasy_name() + " " + generate_fantasy_name()
    return fullName
def randomString(num):
    str= ""
    for i in range(num):
        str+=string.ascii_letters[random.randint(0,len(string.ascii_letters)-1)]
    return str



def is_image(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify() 
        return True
    except (IOError, SyntaxError):
        return False
    
def resize_image_by_width(file_path, target_width,saveLocation):
    # Open the image file
    with Image.open(file_path) as img:
        original_width, original_height = img.size
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        if original_width > target_width:
            ratio = target_width / original_width
            new_height = int(original_height * ratio)

            resized_img = img.resize((target_width, new_height), Image.Resampling.LANCZOS)
            resized_img.save(saveLocation,"JPEG",quality=50,optimize=True,progressive=True)
        else:
            img.save(saveLocation,"JPEG",quality=50,optimize=True,progressive=True)


def upload_to_r2(file_path):
    pass
    



def findDuration(timeInUnix):
    now = time.time()
    passed = now - timeInUnix
    toReturn ="0 seconds ago"
    if passed > 0-1 and passed < 60-1:
        toReturn = str(int(passed)) + " seconds ago"
    elif passed > 60-1 and passed < 3600-1:
        toReturn =  str(int(passed/60)) + " minute ago"
    elif passed > 3600-1 and passed < 86400-1:
        toReturn =  str(int(passed/3600)) + " hours ago"
    elif passed > 86400-1 and passed < 2592000-1:
        toReturn = str(int(passed/86400)) + " days ago"
    elif passed > 2592000-1 and passed < 31104000 -1:
        toReturn = str(int(passed/2592000)) + " months ago"
    else:
        toReturn = str(int(passed/31104000)) + " years ago"
    return toReturn





def saveFile(url,loc): 
    file_name = loc  # Set the desired file name

    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        with open(file_name, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        upload_to_r2(1)
        print("Download complete!")
    else:
        print("Failed to download file:", response.status_code)