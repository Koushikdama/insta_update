from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max
from django.forms import DateTimeField


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    reciepient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")
    body = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    sender_deleted = models.BooleanField(default=False)
    recipient_deleted = models.BooleanField(default=False)
    wallpaper = models.ImageField(upload_to='wallpapers/', null=True, blank=True)
    theme=models.CharField(null=True,blank=True,max_length=20000)

    def sender_message(from_user, to_user, body):
        sender_message = Message(
            user=from_user,
            sender = from_user,
            reciepient = to_user,
            body = body,
            is_read = True
            )
        sender_message.save()
    
        reciepient_message = Message(
            user=to_user,
            sender = from_user,
            reciepient = from_user,
            body = body,
            is_read = True
            )
        reciepient_message.save()
        return sender_message

    def get_message(user):
        users = []
        messages = Message.objects.filter(user=user).values('reciepient').annotate(last=Max('date')).order_by('-last')
        for message in messages:
            users.append({
                'user': User.objects.get(pk=message['reciepient']),
                'last': message['last'],
                'unread': Message.objects.filter(user=user, reciepient__pk=message['reciepient'], is_read=False).count()
            })
        return users
# room and groups
class Topic(models.Model):
    name=models.CharField(max_length=200)
    date=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['date']
    def __str__(self):
        return self.name
class Rooms(models.Model):
    image=models.ImageField(upload_to='rooms-images',default="")
    host=models.ForeignKey(User,on_delete=models.CASCADE)   
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE)
    roomname=models.CharField(max_length=100)
    description=models.TextField(null=True,blank=True)
    members=models.ManyToManyField(User,related_name='members')
    date=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['date']
    def __str__(self):
        return self.topic.name
class Message_group(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    room=models.ForeignKey(Rooms,on_delete=models.CASCADE)
    body=models.TextField(null=True,blank=True)
    date=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['date']
    def __ste__(self):
        return self.user.username
    
    
             
