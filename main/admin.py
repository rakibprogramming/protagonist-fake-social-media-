from django.contrib import admin
from . import models

admin.site.register(models.posts)
# Register your models here.
admin.site.register(models.user)
admin.site.register(models.comment) 
admin.site.register(models.likes) 