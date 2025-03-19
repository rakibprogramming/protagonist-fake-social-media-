from main import utils
import os

files = os.listdir("./static/profileIcons")

for f in files:
    utils.upload_to_r2(".https://pub-6f9406fdeb2544f7acb2423deb3f6e1b.r2.dev/profileIcons/"+f,"protagonist","profileIcons/"+f)
    print("uploaded "+f)