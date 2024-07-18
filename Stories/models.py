from django.db import models
from django.db.models.signals import post_save
import uuid
from django.contrib.auth.models import User
from Post.models import Follow

# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class StoryFileContent(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_story_owner')
	file = models.FileField(upload_to=user_directory_path)
class Story(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='story_user')
	content =  models.ManyToManyField(StoryFileContent, related_name='content_user')
	caption = models.TextField(max_length=50)
	expired = models.BooleanField(default=False)
	posted = models.DateTimeField(auto_now_add=True)

	def get_absolute_url(self):
		return reverse('showmedia', args=[str(self.id)])

	def __str__(self):
		return str(self.id)

	def __str__(self):
		return self.user.username

class StoryStream(models.Model):
	following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='story_following')
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	#story = models.ManyToManyField(Story, related_name='storiess')
	story = models.ForeignKey(Story, on_delete=models.CASCADE, null=True)
	date = models.DateTimeField(auto_now_add=True)
	read=models.BooleanField(default=False)

	def __str__(self):
		return self.following.username + ' - ' + str(self.date)+'-'+str(self.user)

	def add_post(sender, instance, *args, **kwargs):
		new_story = instance
		user = new_story.user
		followers = Follow.objects.all().filter(following=user)

		for follower in followers:
			stream=StoryStream(story=new_story,user=follower.follower,date=new_story.posted,following=user)
			stream.save()

# Story Stream
post_save.connect(StoryStream.add_post, sender=Story)
