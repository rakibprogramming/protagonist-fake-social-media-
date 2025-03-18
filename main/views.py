from django.shortcuts import render,HttpResponse
import json
import time
import requests
from . import utils
from . import models
import os
from django.utils.html import escape

import random
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
        userId = req.COOKIES.get("identifier")
        userId = list(models.user.objects.filter(sessonId = userId).values())[0]["userId"]
        postId = utils.randomString(10)
        hasImage = "0"
        timeIs = str(time.time())
        uploaded_file = req.FILES.get('file')
        if uploaded_file:
            tmpLocation = utils.randomString(20)
            tmpimageLocation= "./static/tmp/" + tmpLocation
            with open(tmpimageLocation, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            if utils.is_image(tmpimageLocation):
                hasImage = "1"
                utils.resize_image_by_width(tmpimageLocation,1000,"./static/tmp/"+postId+".jpg")
                utils.upload_to_r2(file_path="./static/tmp/"+postId+".jpg",bucket_name="protagonist",object_name="postImage/"+postId+".jpg")
                os.remove("./static/tmp/"+postId+".jpg")
            os.remove(tmpimageLocation)
            
        models.posts(userId=userId,postId=postId,hasImage=hasImage,text=textdata,time=timeIs).save()

        return HttpResponse('{"id": "'+postId+'"}') 
    else:
        return HttpResponse('{"id": "error"}')

def addingcomment(req):
    if req.method == "POST":
        userId = req.COOKIES.get("identifier")
        username = list(models.user.objects.filter(sessonId = userId).values())[0]["userName"]
        userId = list(models.user.objects.filter(sessonId = userId).values())[0]["userId"]
        commentId = utils.randomString(10)
        commentText = req.POST.get("commentText")
        postID = req.POST.get("postId")
        commentTime = str(time.time())
        models.comment(commentText=commentText,postId=postID,commentId=commentId,time=commentTime, userId=userId, userName=username).save()

        return HttpResponse("DONE")



def nameGenerator(r):
    return HttpResponse(utils.nameGenerator()) 

def postView(req,id):
    urserID = req.COOKIES.get("identifier")
    SLEFuserId = list(models.user.objects.filter(sessonId = urserID).values())[0]["userId"]
    postModel = models.posts.objects.filter(postId = id)
    numberOfPost = len(postModel.values())
    if numberOfPost == 1:
        postValues = list(postModel.values())[0]
        userId = postValues["userId"]
        caption = postValues["text"]
        image = postValues["hasImage"]
        print(userId)
        userInfo = list(models.user.objects.filter(userId = userId).values())[0]
        userName = userInfo["userName"]
        comment = list(models.comment.objects.filter(postId = id).values())
        numOfComment = len(models.comment.objects.filter(postId = id))
        postInfo = {
            "userName" : userName,
            "userId" : userId,
            "caption" : caption, 
            "postId" : id,
            "comments": comment,
            "numOfComment" : numOfComment,
            "likeState": "likes",
            "numOfLike" : len(models.likes.objects.filter(postId = id))
        }
        if len(models.likes.objects.filter(userId = SLEFuserId, postId = id)) !=0:
           postInfo["likeState"] = "liked" 
        
        if image == "1":
            postInfo["hasImage"] = "1"
        return render(req,"post.html",context=postInfo) 
    else:
        return HttpResponse("not found")
    


def sendPostData(req):
    urserID = req.COOKIES.get("identifier")
    userId = list(models.user.objects.filter(sessonId = urserID).values())[0]["userId"]
    realdata= []
    datas = list(models.posts.objects.values())
    for i in datas:
        userInfo = list(models.user.objects.filter(userId = i['userId']).values())[0]
        userName = userInfo["userName"]
        i["likeState"] = "likes"
        i["username"] = userName
        i["text"] = escape(i["text"])
        i["numOfPost"] = len(models.comment.objects.filter(postId = i["postId"]))
        i["numOfLike"] = len(models.likes.objects.filter(postId = i["postId"]))
        
        if len(models.likes.objects.filter(userId = userId, postId = i["postId"])) !=0:
           i["likeState"] = "liked" 
        realdata.append(i)
    random.shuffle(realdata)
    contx = {
        'posts':realdata
    }
     
    return render(req,"postrender.html",context=contx)

def addLike(req):
    if req.method == "POST":
        urserID = req.COOKIES.get("identifier")
        userId = list(models.user.objects.filter(sessonId = urserID).values())[0]["userId"]
        postId = req.POST.get("postID")
        remove = req.POST.get("remove","no")
        if remove == "no":
            adding = models.likes(userId = userId, postId = postId)
            adding.save()
        else:
            models.likes.objects.filter(postId = postId, userId = userId).delete()
            return HttpResponse("DONE")

 
    return HttpResponse("NOT DONE")