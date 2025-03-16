from django.shortcuts import render,HttpResponse
import json
import time
import requests
from . import utils
from . import models
import PIL

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
        userId = req.COOKIES.get("identifier")
        userId = list(models.user.objects.filter(sessonId = userId).values())[0]["userId"]
        postId = utils.randomString(10)
        hasImage = "0"
        uploaded_file = req.FILES.get('file')
        if uploaded_file:
            hasImage = "1"
            with open("./static/postImage/" + uploaded_file.name, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
        models.posts(userId=userId,postId=postId,hasImage=hasImage,text=textdata).save()

        return HttpResponse('{"id": "'+postId+'"}') 
    else:
        return HttpResponse('{"id": "error"}')

def nameGenerator(r):
    return HttpResponse(utils.nameGenerator()) 

def postView(req,id):
    postModel = models.posts.objects.filter(postId = id)
    numberOfPost = len(postModel.values())
    if numberOfPost == 1:
        postValues = list(postModel.values())[0]
        userId = postValues["userId"]
        caption = postValues["text"]
        print(userId)
        userInfo = list(models.user.objects.filter(userId = userId).values())[0]
        userName = userInfo["userName"]
        postInfo = {
            "userName" : userName,
            "userId" : userId,
            "caption" : caption, 
        }
        return render(req,"post.html",context=postInfo) 
    else:
        return HttpResponse("not found")