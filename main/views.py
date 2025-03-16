from django.shortcuts import render,HttpResponse
import json
import time
import requests
from . import utils
from . import models


def homepage(r):
    response = render(r,"index.html")
    response.set_cookie("test","home")
    useridintifier = r.COOKIES.get("identifier")
    if not useridintifier:
        session = utils.randomString(100)
        response.set_cookie("identifier",session)
        userName = utils.nameGenerator()
        userId = userName.replace(" ","")
        userId = userId.lower()
        addUser = models.user(userId = userId, sessonId = session, userName = userName)
        addUser.save()
        utils.saveFile("https://picsum.photos/100","./static/profileIcons/"+userId+".jpg")
    return response


def notificationPage(r):
    response = render(r,"notification.html")
    useridintifier = r.COOKIES.get("identifier")
    if not useridintifier:
        session = utils.randomString(100)
        response.set_cookie("identifier",session)
        userName = utils.nameGenerator()
        userId = userName.replace(" ","")
        userId = userId.lower()
        addUser = models.user(userId = userId, sessonId = session, userName = userName)
        addUser.save()
        utils.saveFile("https://picsum.photos/100","./static/profileIcons/"+userId+".jpg")
    response.set_cookie("test","notiification")
    return response


def profilePage(r):
    useridintifier = r.COOKIES.get("identifier")
    if not useridintifier:
        session = utils.randomString(100)
        userName = utils.nameGenerator()
        userId = userName.replace(" ","")
        response = render(r,"profile.html",{"userid":userId,"name":userName})
        response.set_cookie("identifier",session,max_age=60*60*24*30)
        userId = userId.lower()
        addUser = models.user(userId = userId, sessonId = session, userName = userName)
        addUser.save()
        utils.saveFile("https://picsum.photos/100","./static/profileIcons/"+userId+".jpg")
    else:
        datas = models.user.objects.filter(sessonId = useridintifier).values()
        print(datas)
        userId = datas[0]["userId"]
        userName = datas[0]["userName"]
        response = render(r,"profile.html",{"userid":userId,"name":userName})
    return response

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

def nameGenerator(r):
    return HttpResponse(utils.nameGenerator()) 