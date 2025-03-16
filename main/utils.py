import requests
import random
import string
def nameGenerator():
    races="dragonborn,dwarf,elf,gnome,goblin,half-elf,half-orc,halfling,human,orc,tiefling,troll".split(",")
    nameData = requests.get("https://names.ironarachne.com/race/"+random.choice(races)+"/male/2").json()
    fullName = nameData["names"][0] + " " + nameData["names"][1]
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
