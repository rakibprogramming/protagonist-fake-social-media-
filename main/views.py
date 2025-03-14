from django.shortcuts import render,HttpResponse
import json
import time
from . import models
def homepage(r):
    return render(r,"index.html")


def notificationPage(r):
    return   render(r,"notification.html")


def profilePage(r):
    return render(r,"profile.html")

def test(r):
    if r.method == "POST":
        data = json.loads(r.body)
        print(data)
    return HttpResponse("{status: 'done'}")


def validitingPostData(req):
    if req.method == "POST":
        textdata = req.POST.get('postText')
        print(textdata)
        userId = 'dummy'
        postId = "dummy"
        hasImage = "0"
        uploaded_file = req.FILES.get('file')
        if uploaded_file:
            hasImage = "1"
            with open("./static/postImage/" + uploaded_file.name, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
        models.posts(userId=userId,postId=postId,hasImage=hasImage,text=textdata).save()

    return HttpResponse("{status: 'done'}") 