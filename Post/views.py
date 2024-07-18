from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from Post.models import Stream,Post,Tag,Likes,PostFileContent
from django.urls import reverse
from authy.models import Profile
from Post.forms import NewPostForm
from Comment.forms import CommentForm
from Comment.models import Comment
from Stories.models import Story, StoryStream
from django.contrib.auth.models import User
from authy.sendmail import sendmail
from django.http import JsonResponse
from django.utils.html import mark_safe
from django.utils.safestring import mark_safe
import json
from django.core.serializers import serialize
from Post.models import Follow









# Create your views here.
@login_required
def index(request):
	user = request.user
	user = get_object_or_404(User, username=request.user)
	login_profile = Profile.objects.get(user=user)
	print("profile",login_profile.picture)
	
	posts = Stream.objects.filter(user=user)

	stories = StoryStream.objects.filter(user=user)
	
	
	all_users = Profile.objects.all()
	#print("profile",all_users)


	group_ids = []
	post_liked=[]
	post_saved=[]
	story_ids=[]

	for post in posts:
		group_ids.append(post.post_id)
	for story in stories:
		
		story_ids.append(story.story_id)
	
		
	story_items=Story.objects.filter(id__in=story_ids).all().order_by('-posted')
	print('story_items',type(story_items))
	post__items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')
	for i in story_items:
		print(i)
	#print(post__items)
	for post_item in post__items:
		post = Post.objects.get(id=post_item.id)
		like=Likes.objects.filter(user=user, post=post).exists()
		post_liked.append(like)
		profile = Profile.objects.get(user=user)
		save=profile.favorites.filter(id=post_item.id).exists()
		post_saved.append(save)

	post_items=list(zip(post__items,post_liked,post_saved))

	template = loader.get_template('index.html')
	
	
	context = {
		'post_items': post_items,
		'stories': story_items,
		'login_user':login_profile

	}

	return HttpResponse(template.render(context, request))

@login_required
def NewPost(request):
	user = request.user
	tags_objs = []
	files_objs=[]
	

	if request.method == 'POST':
		form = NewPostForm(request.POST,request.FILES)
		if form.is_valid():
			files = request.FILES.getlist('picture')
			
			caption = form.cleaned_data.get('caption')
			tags_form = form.cleaned_data.get('tags')

			tags_list = list(tags_form.split(','))

			for tag in tags_list:
				t, created = Tag.objects.get_or_create(title=tag)
				tags_objs.append(t)
			
			for file in files:
				file_instance = PostFileContent(file=file, user=user)
				file_instance.save()
				files_objs.append(file_instance)

			files_objs.append(file_instance)
			p, created = Post.objects.get_or_create(caption=caption, user=user)
			p.tags.set(tags_objs)
			p.picture.set(files_objs)
			p.save()
			return redirect('index')
	else:
		form = NewPostForm()

	context = {
		'form':form,
	}

	return render(request, 'newpost.html', context)


def PostDetails(request, post_id):
	post = get_object_or_404(Post, id=post_id)
	print("post_index",post)
	user = request.user
	profile=Profile.objects.get(user=request.user)
	favorited=False
	#comment
	comments = Comment.objects.filter(post=post).order_by('date')

	if (request.user.is_authenticated):
		profile=Profile.objects.get(user=request.user)
		if(profile.favorites.filter(id=post_id).exists()):
			favorited=True
			#Comments Form
	if request.method == 'POST':
		form = CommentForm(request.POST)
	#	form=request.POST.get['comment']
		#-> html elements ->print(form)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.user = user
			comment.save()
			return HttpResponseRedirect(reverse('postdetails', args=[post_id]))
	else:
		form = CommentForm()
		
	context={
		'post':post,
		'favorited':favorited,
		'form':form,
		'comments':comments,
	}
	
	return render(request,'post_detail.html',context)
	
	
def tags(request, tag_slug):
	tag = get_object_or_404(Tag, slug=tag_slug)
	posts = Post.objects.filter(tags=tag).order_by('-posted')

	template = loader.get_template('tag.html')

	context = {
		'posts':posts,
		'tag':tag,
	}

	return HttpResponse(template.render(context, request))
	

@login_required
def like(request, post_id):
	post = get_object_or_404(Post, id=post_id)
	user = request.user
	post = Post.objects.get(id=post_id)
	current_likes = post.likes
	list=[]
 # posted -> user  profile object
	user_id=User.objects.get(username=post.user.username)
	receiver_user=get_object_or_404(Profile, user=user_id)
 #############
	
	liked = Likes.objects.filter(user=user, post=post).count()
	#print(liked)

	if not liked:
		like = Likes.objects.create(user=user, post=post)
		#like.save()
		# posted username -> print("like",post.user.username)
		
		# print user profile object -> print("receiver_user",receiver_user.is_send_notifications)
		if(receiver_user.is_send_notifications == 'yes'):
			#print("email",receiver_user.user.email)
			sendmail(receiver_user.user.email,receiver_user.user.username,2,request.user)
		current_likes = current_likes + 1
		colors=False
		#print("after chamge ",current_likes)
		

	else:
		Likes.objects.filter(user=user, post=post).delete()
		if(receiver_user.is_send_notifications == 'yes'):
    			#print("email",receiver_user.user.email)
			sendmail(receiver_user.user.email,receiver_user.user.username,3,request.user)
		current_likes = current_likes - 1
		#print("after chamge ",)
		colors=True
    	
		
		
	post.likes = current_likes
	post.save()

	#return HttpResponseRedirect(reverse('postdetails', args=[post_id]))
	#return HttpResponseRedirect(reverse('index', args=[post_id]))

	return JsonResponse({'likes':current_likes,'status':colors})
	
	
	
	
	

@login_required
def favorite(request, post_id):
	user = request.user
	post = Post.objects.get(id=post_id)
	profile = Profile.objects.get(user=user)

	if profile.favorites.filter(id=post_id).exists():
		profile.favorites.remove(post)
		saved=False

	else:
		profile.favorites.add(post)
		saved=True
	#print(saved)

	#return HttpResponseRedirect(reverse('postdetails', args=[post_id]))
	return JsonResponse({'status':saved})



def search_user(request, search_user):
    all_posts_title = User.objects.filter(username__icontains=search_user).values('username')
    all_posts_description = Profile.objects.filter(first_name__icontains=search_user).values("first_name")
    all_posts = list(all_posts_title) + list(all_posts_description)
    print('all_posts',all_posts)

    if len(all_posts) == 0:
        pass
    else:
        user = get_object_or_404(User, username=search_user)
        profile = Profile.objects.filter(user=user).first()
        following_count = Follow.objects.filter(follower=user).count()
        print("following",following_count)
        followers_count = Follow.objects.filter(following=user).count()
        print("follower",followers_count)
        details = json.dumps({'username': user.username, 'first_name': profile.first_name,"picture":str(profile.picture),'following':following_count,'followers':followers_count})
        print(details)
        return JsonResponse(details, safe=False)
  
