from django.shortcuts import render,HttpResponse

def homepage(r):
    return render(r,"index.html")


def notificationPage(r):
    return   render(r,"notification.html")


def profilePage(r):
    return render(r,"profile.html")