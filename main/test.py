import requests
import random
def nameGenerator():
    races="dragonborn,dwarf,elf,gnome,goblin,half-elf,half-orc,halfling,human,orc,tiefling,troll".split(",")
    nameData = requests.get("https://names.ironarachne.com/race/"+random.choice(races)+"/male/2").json()
    fullName = nameData["names"][0] + " " + nameData["names"][1]
    print(fullName)

nameGenerator()