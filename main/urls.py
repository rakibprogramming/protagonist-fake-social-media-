from django.urls import path
from . import views

urlpatterns = [
    path("",views.homepage),
    path("activity",views.notificationPage),
    path("profile",views.profilePage)
]
 