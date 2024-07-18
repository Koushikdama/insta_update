from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize

from datetime import datetime


import json
from datetime import datetime

	

# Create your views here.
from Stories.models import Story, StoryStream,StoryFileContent
from Stories.forms import NewStoryForm

from datetime import datetime, timedelta
from authy.models import Profile


@login_required
def NewStory(request):
	user = request.user
	file_objs = []

	if request.method == "POST":
		form = NewStoryForm(request.POST, request.FILES)
	
		if form.is_valid():
			files = request.FILES.getlist('content')
			
			caption = form.cleaned_data.get('caption')
			for file in files:
				story = StoryFileContent(user=user, file=file)
				story.save()
				file_objs.append(story)
			s, created = Story.objects.get_or_create(caption=caption, user=user)
			s.content.set(file_objs)
			s.save()

			return redirect('index')
	else:
		form = NewStoryForm()

	context = {
		'form': form,
	}

	return render(request, 'newstory.html', context)


# def ShowMedia(request, stream_id):
# 	"""user = get_object_or_404(Story, id=stream_id)
# 	user_id=User.objects.get(username=user)
# 	receiver_user=get_object_or_404(Profile, user=user_id)"""
# 	post = get_object_or_404(Story, id=stream_id)
# 	print("story_kk",post)
 
 
	# stories = StoryStream.objects.get(id=stream_id)
	# print("stories",stories.read)
	# stories.read=True
	# stories.save()
	# print("stories",stories.read)
	
	# media_st = stories.story.all().values()
	# print("media_st",media_st)
	# stories_list = list(media_st)
 
	# print("stories after",stories.read)
	
	
	
	# return JsonResponse(stories_list, safe=False)
def ShowMedia(request, stream_id):
	print(stream_id)
	story = get_object_or_404(Story, id=stream_id)
	story.read=True
	user = request.user
	profile = Profile.objects.get(user=user)
	post = get_object_or_404(Story, id=stream_id)
	print("ShowMedia_post",type(post))
	print('ShowMedia_story',type(story))
	

	#template = loader.get_template('post_detail.html')
	print("story_user_name",story.user.username)
	print("story_",story.content.all())
	for i in story.content.all():
		print(i.file)
	story={
		'username':story.user.username,
		'posted':story.posted.isoformat(),
		'caption':story.caption,
		'content':[i.file.url for i in story.content.all() ],
		'is_read':story.read
	}
	print("finnaly_story",story)
	story_json = json.dumps(story)

	

	#return HttpResponse(template.render(context, request))
	
	return JsonResponse(story_json, safe=False)
	#return HttpResponse("hii")
