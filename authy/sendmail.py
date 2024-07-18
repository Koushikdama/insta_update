import uuid
from django.conf import settings
from django.core.mail import send_mail

def sendmail(email,sendername,option,loginame):
    answer=[" unfollow you","follow you ","your post has been  liked by ","your post has been unlike by "]
   
    subject = f'dear {sendername}'
    message = f'Dear \t {sendername }\t {loginame } \t { answer[option]}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )