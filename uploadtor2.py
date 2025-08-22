from main import utils
import os

files = os.listdir("./static/profileIcons")

for f in files:
    utils.upload_to_r2("./statics/profileIcons/"+f,"protagonist","profileIcons/"+f)
    print("uploaded "+f)