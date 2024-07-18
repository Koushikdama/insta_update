from django.contrib import admin

from Stories.models import Story, StoryStream

# Register your models here.

admin.site.register(Story)
admin.site.register(StoryStream)