from django.urls import path
from Stories.views import NewStory, ShowMedia

urlpatterns = [
	path('newstory/', NewStory, name='newstory'),
	path('showmedia/<uuid:stream_id>', ShowMedia, name='showmedia'),
]