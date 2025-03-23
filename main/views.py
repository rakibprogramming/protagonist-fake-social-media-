from django.shortcuts import render,HttpResponse
import json
import time
import requests
from . import utils
from . import models
import os
from django.utils.html import escape
import random
from .ai import groqai
import threading

def addNotification(byWho,toWho,message,redirecto):
    timeNow = str(time.time())
    models.notification(byWho=byWho, toWho = toWho, message = message, redirectiTo = redirecto,time=timeNow).save()
def addpost(forWho):
    lastToObject = list(models.posts.objects.filter(ai="no",forWho = forWho).values())
    random.shuffle(lastToObject)
    lastToObject = lastToObject[:30]
    lastToObjectText = "{ "
    for obj in lastToObject:
        obj = obj['text']   
        lastToObjectText += " ["+obj+"]," 
    lastToObjectText = lastToObjectText +  "}"
    postText = groqai.getPost(lastToObjectText)
    userId = random.choice(list(models.user.objects.filter(ai = "yes").values()))["userId"]
    postId = utils.randomString(10)
    models.posts(userId=userId,postId=postId,hasImage="0",text=postText,time=str(time.time()),ai="yes",forWho = forWho).save()


def homepage(r):
    
    userName = utils.nameGenerator()
    userId = userName.replace(" ","")
    userId = userId.lower()
    response = render(r,"index.html",context={"userid":userId})
    response.set_cookie("test","home")
    useridintifier = r.COOKIES.get("identifier")

    if not useridintifier:
        session = utils.randomString(100)
        response.set_cookie("identifier",session, max_age=60*60*24*30)
        addUser = models.user(userId = userId, sessonId = session, userName = userName)
        addUser.save()
        utils.saveFile("https://picsum.photos/100","./static/profileIcons/"+userId+".jpg")
    else:
        me = list(models.user.objects.filter(sessonId= useridintifier).values())[0]["userId"]
        response = render(r,"index.html",context={"userid":me})

        addAIPostThread = threading.Thread(target=addpost,args=(me,))
        addAIPostThread.start()
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
        utils.saveFile("https://picsum.photos/100",".https://pub-6f9406fdeb2544f7acb2423deb3f6e1b.r2.dev/profileIcons/"+userId+".jpg")
    else:
        userId = list(models.user.objects.filter(sessonId = useridintifier).values())[0]['userId']
        notifications = list(models.notification.objects.filter(toWho = userId).values())
        realdata=[]
        for i in notifications:
            i["senderName"] = list(models.user.objects.filter(userId=i["byWho"]).values())[0]["userName"]
            i["recieaverName"] = list(models.user.objects.filter(userId=i["toWho"]).values())[0]["userName"]
            i['time'] = utils.findDuration(float(i["time"]))
            realdata.append(i)
        realdata.reverse()
        contex = {"noti":realdata }
        response = render(r,"notification.html",context=contex)
    response.set_cookie("test","notiification")
    return response


def profilePage(r):
    useridintifier = r.COOKIES.get("identifier")
    progileUSerId = r.GET.get("userid","notSet")
    if progileUSerId == "notSet" and useridintifier:
        progileUSerId = list(models.user.objects.filter(sessonId=useridintifier).values())[0]["userId"]
    if not useridintifier:
        session = utils.randomString(100)
        userName = utils.nameGenerator()
        userId = userName.replace(" ","").lower()
        response = render(r,"profile.html",{"userid":userId,"name":userName,"profileuserid":userId})
        response.set_cookie("identifier",session,max_age=60*60*24*30)
        userId = userId.lower()
        addUser = models.user(userId = userId, sessonId = session, userName = userName)
        addUser.save()
        utils.saveFile("https://picsum.photos/100",".https://pub-6f9406fdeb2544f7acb2423deb3f6e1b.r2.dev/profileIcons/"+userId+".jpg")
    else:
        datas = models.user.objects.filter(sessonId = useridintifier).values()
        print(datas)
        if progileUSerId == "notSet":
            userId = datas[0]["userId"] 
            userName = datas[0]["userName"]
        else:
            userId = progileUSerId
            userName = list(models.user.objects.filter(userId = userId).values())[0]["userName"] 
        response = render(r,"profile.html",{"userid":userId,"name":userName,"profileuserid":progileUSerId})
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
        iamgeExplanation = "NA"
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
                iamgeExplanation = groqai.groqimage("https://pub-6f9406fdeb2544f7acb2423deb3f6e1b.r2.dev/postImage/"+postId+".jpg")
                os.remove("./static/tmp/"+postId+".jpg") 
            os.remove(tmpimageLocation)
            
        models.posts(userId=userId,postId=postId,hasImage=hasImage,text=textdata,time=timeIs,imageDiscription=iamgeExplanation, forWho = userId).save()

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
        poserId = list(models.posts.objects.filter(postId = postID).values())[0]["userId"]
        addNotification(byWho=userId,toWho=poserId,message="Commented on Your Post",redirecto="/post/"+postID)
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
        timePassed = utils.findDuration(float(postValues['time']))
        print(userId)
        userInfo = list(models.user.objects.filter(userId = userId).values())[0]
        userName = userInfo["userName"]
        comment = list(models.comment.objects.filter(postId = id).values())
        comment.reverse() 
        numOfComment = len(models.comment.objects.filter(postId = id))
        postInfo = {
            "userName" : userName,
            "userId" : userId,
            "caption" : caption, 
            "postId" : id,
            "comments": comment,
            "numOfComment" : numOfComment,
            "likeState": "likes",
            "numOfLike" : len(models.likes.objects.filter(postId = id)),
            "timePassed": timePassed
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
    lastId = int(req.POST.get("lastId"))
    datas = list(models.posts.objects.filter(forWho=userId).values().order_by('-id')[:10][::-1])
    if lastId > 0:
        print("now doing this", lastId)
        datas = list(models.posts.objects.filter(id__lte=lastId,forWho = userId).values().order_by('-id')[:10]) 
        datas.reverse() 
    if len(datas) > 0:
        newLastScrool = datas[0]["id"] 
    else:
        newLastScrool = 0 
    print(newLastScrool) 
    for i in datas: 
        userInfo = list(models.user.objects.filter(userId = i['userId']).values())[0]
        userName = userInfo["userName"]
        i["likeState"] = "likes" 
        i["username"] = userName
        i["text"] = escape(i["text"])
        i["numOfPost"] = len(models.comment.objects.filter(postId = i["postId"]))
        i["numOfLike"] = len(models.likes.objects.filter(postId = i["postId"]))
        i["timePassed"] = utils.findDuration(float(i['time']))
        
        if len(models.likes.objects.filter(userId = userId, postId = i["postId"])) !=0:
           i["likeState"] = "liked" 
        realdata.append(i) 
    realdata.reverse() 
    contx = {
        'posts':realdata,
        "lastScrool":newLastScrool 

    }
     
    return render(req,"postrender.html",context=contx)


def sendUserPostData(req):
    urserID = req.COOKIES.get("identifier")
    userId = list(models.user.objects.filter(sessonId = urserID).values())[0]["userId"]
    realdata= []
    postUserId = req.POST.get("userID")
    datas = list(models.posts.objects.filter(userId=postUserId).values())
    newLastScrool = 1
    if len(datas) > 0:
        for i in datas:
            userInfo = list(models.user.objects.filter(userId = i['userId']).values())[0]
            userName = userInfo["userName"]
            i["likeState"] = "likes"
            i["username"] = userName
            i["text"] = escape(i["text"])
            i["numOfPost"] = len(models.comment.objects.filter(postId = i["postId"]))
            i["numOfLike"] = len(models.likes.objects.filter(postId = i["postId"]))
            i["timePassed"] = utils.findDuration(float(i['time']))
            
            if len(models.likes.objects.filter(userId = userId, postId = i["postId"])) !=0:
                i["likeState"] = "liked" 
            realdata.append(i) 
        realdata.reverse() 
    contx = {
        'posts':realdata,
        "lastScrool":newLastScrool 

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
            poserId = list(models.posts.objects.filter(postId = postId).values())[0]["userId"]
            addNotification(byWho=userId,toWho=poserId,message="Liked on Your Post",redirecto="/post/"+postId)
        else:
            models.likes.objects.filter(postId = postId, userId = userId).delete()
            return HttpResponse("DONE")
        
    return HttpResponse("NOT DONE")


def createAiUSer(req,ammount):
    for a in range(ammount):
        userName = utils.nameGenerator()
        userId = userName.replace(" ","")
        userId = userId.lower()
        session = utils.randomString(100)
        addUser = models.user(userId = userId, sessonId = session, userName = userName,ai="yes")
        addUser.save()
        utils.saveFile("https://picsum.photos/100","./static/profileIcons/"+userId+".jpg")
        utils.upload_to_r2("./static/profileIcons/"+userId+".jpg","protagonist","profileIcons/"+userId+".jpg")   
        print("Added ",userId)
    return HttpResponse(ammount+32132)  

def addAIComment(req):
    if req.method == "POST":
        urserID = req.COOKIES.get("identifier")
        realuserId = list(models.user.objects.filter(sessonId = urserID).values())[0]["userId"]
        lastToObject = list(models.posts.objects.filter(ai="no",forWho=realuserId).values())
        lastToObject.reverse()
        lastToObject = lastToObject[:30] 
        lastToObjectText = "{ "
        for obj in lastToObject: 
            obj = obj['text']  
            lastToObjectText += " ["+obj+"]," 
        lastToObjectText = lastToObjectText +  "}"
 
        postId = req.POST.get("postId")
        users = list(models.user.objects.filter(ai="yes").values())
        postData = list(models.posts.objects.filter(postId=postId).values())[0]
        caption = postData["text"]
        hasimage = postData["hasImage"]
        imageExplanation = postData["imageDiscription"]
        if hasimage == "0":
            comments = groqai.getCommentForPost(caption=caption,context = lastToObjectText)
        else:
            comments = groqai.getCommentForPost(caption=caption,image = "yes", imageExpl = imageExplanation, context = lastToObjectText)

        numberofComment = len(models.comment.objects.filter(postId = postId))
        do = True
        print(numberofComment) 
        if numberofComment > 100: 
            do = False
            print("COmments are more than 100 to doing toss")
            if 3 == random.randint(1,3):
                do = True
        if do:
            for i in comments:
                randomUser = random.choice(users)["userId"]
                userName = list(models.user.objects.filter(userId = randomUser).values())[0]["userName"]
                postUser = list(models.posts.objects.filter(postId = postId).values())[0]["userId"]
                models.comment(commentText=i,postId=postId,commentId=utils.randomString(10),time=str(time.time()), userId=randomUser, userName=userName).save()
                addNotification(byWho=randomUser,toWho=postUser,message="Commented on Your Post",redirecto="/post/"+postId)
        for a in range(random.randint(1,20)):
                models.likes(userId = utils.randomString(10), postId = postId).save()

        return HttpResponse(postId) 
 

def renderComments(req):
    id = req.GET.get("id")
    comment = list(models.comment.objects.filter(postId = id).values())
    comment.reverse()
    context = {"comments":comment}
    return render(req,"commentrender.html",context=context)