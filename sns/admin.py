from django.contrib import admin
from .models import Message,Group,Friend,Good

admin.site.register(Message)
admin.site.register(Group)
admin.site.register(Friend)
admin.site.register(Good)