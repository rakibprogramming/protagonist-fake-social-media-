import requests
import random
import string
from PIL import Image
import boto3
from botocore.exceptions import ClientError
import os

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

def saveFile(url,loc): 
    file_name = loc  # Set the desired file name

    response = requests.get(url, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        with open(file_name, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print("Download complete!")
    else:
        print("Failed to download file:", response.status_code)

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
            resized_img.save(saveLocation,"JPEG")
        else:
            img.save(saveLocation,"JPEG")


def upload_to_r2(file_path, bucket_name, object_name, account_id=None, access_key_id=None, secret_access_key=None):

    # Check if file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File {file_path} not found")

    # Get credentials from environment variables if not provided
    account_id = account_id or os.getenv('CLOUDFLARE_ACCOUNT_ID')
    access_key_id = access_key_id or os.getenv('CLOUDFLARE_R2_ACCESS_KEY_ID')
    secret_access_key = secret_access_key or os.getenv('CLOUDFLARE_R2_SECRET_ACCESS_KEY')

    # Validate credentials
    if not all([account_id, access_key_id, secret_access_key]):
        raise ValueError(
            "Missing credentials. Provide them as arguments or set these environment variables: "
            "CLOUDFLARE_ACCOUNT_ID, CLOUDFLARE_R2_ACCESS_KEY_ID, CLOUDFLARE_R2_SECRET_ACCESS_KEY"
        )

    # Create R2 client
    client = boto3.client(
        's3',
        region_name='auto',
        endpoint_url=f'https://{account_id}.r2.cloudflarestorage.com',
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key
    )

    # Upload file
    try:
        client.upload_file(file_path, bucket_name, object_name)
        print(f"Successfully uploaded {file_path} to {bucket_name}/{object_name}")
        return True
    except ClientError as e:
        print(f"Upload failed: {e}")
        return False
    



