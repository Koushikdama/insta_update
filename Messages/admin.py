from django.contrib import admin
from Messages.models import Message,Message_group,Rooms,Topic

admin.site.register(Message)
admin.site.register(Message_group)
admin.site.register(Topic)
admin.site.register(Rooms)