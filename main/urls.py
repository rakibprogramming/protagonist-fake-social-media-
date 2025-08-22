from django.urls import path
from . import views

urlpatterns = [
    path("",views.homepage),
    path("activity",views.notificationPage),
    path("profile",views.profilePage),
    path("test", views.test),
    path("validatedata", views.validitingPostData),
    path("getarandomname", views.nameGenerator),
    path("post/<str:id>",views.postView),
    path("getpost",views.sendPostData),
    path("getuserpost",views.sendUserPostData),
    path("addcomment",views.addingcomment),
    path("addlike",views.addLike),
    path("createaiuser/<int:ammount>",views.createAiUSer),
    path("addaicomment",views.addAIComment),
    path("rendercomment",views.renderComments),
    path("statics/<path:fileName>",views.serveStatic)
]
 