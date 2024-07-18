
from django.shortcuts import redirect, render, get_object_or_404,HttpResponsePermanentRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from Messages.models import Message
from django.contrib.auth.models import User
from authy.models import Profile
from django.db.models import Q
from django.core.paginator import Paginator
from Post.models import Stream,Post,Follow

@login_required
def inbox(request):
    user = request.user
    #print("inbox",user)
    messages = Message.get_message(user=request.user)
    active_direct = None
    directs = None
    profile = get_object_or_404(Profile, user=user)
    #print("profile",profile.user.username)
    #print("messages",messages)

    if messages:
        #print("message",messages)
        message = messages[0]
        active_direct = message['user'].username
        active_user=active_direct
        #print("activate_user",active_user)
        user = get_object_or_404(User, username=active_direct)
        profile_receiver=None
        profile_receiver = Profile.objects.get(user=user)
        #print("active",profile_receiver.user.username)
        directs = Message.objects.filter(user=request.user, reciepient=message['user'])
        directs.update(is_read=True)
        a=""
        b=""
        for i in directs:
            print("i",i.body)
            a=i.theme
            print("a",a)
            if(a != None):
                print(a != None )
                b=a
                a=b
                print("if yes")
            else:
                print("befor update",i.theme)
                i.theme=b
                i.save()
                print("after update",i.theme)
        else:
            directs = Message.objects.filter(user=request.user, reciepient=message['user'])
            directs.update(is_read=True)
            for i in directs:
                color=[i.theme]
                print(a)
                b=color.pop()
                print("b",b)
            
        for message in messages:
            if message['user'].username == active_direct:
                message['unread'] = 0
       
        
    
        context = {
        'directs':directs,
        'messages': messages,
        'active_direct': active_direct,
        'profile': profile,
        'profile_receiver':profile_receiver,
        'theme':b
        
        }
        return render(request, 'directs/message.html', context)
    else:
        all_user=[]
        user = get_object_or_404(User, username=request.user)
        followings=Follow.objects.filter(follower=user)
        followers=Follow.objects.filter(following=user)
        if(followings.exists()):
            for i in followings:
                user = get_object_or_404(User, username=i.following.username)
                profile = Profile.objects.get(user=user)
                all_user.append(profile)
                print("user_following",user)
        if(followers.exists()):
            for i in followers :
                user = get_object_or_404(User, username=i.following.username)
                profile = Profile.objects.get(user=user)
                all_user.append(profile)
        print("use_follower",all_user)
        for i in all_user:
            print(i.user.username)
        context={
            'all_user':all_user
        }
            
        return render(request, 'directs/search.html',context)
    


@login_required
def Directs(request, username):
    user  = request.user
    selected_user= get_object_or_404(User, username=username)    
    profile_search_selecter = Profile.objects.get(user=selected_user)
    messages = Message.get_message(user=user)
    active_direct = username
    directs = Message.objects.filter(user=user, reciepient__username=username)  
    directs.update(is_read=True)
    print("directs::",directs)
    a=""
    for i in directs:
            a=i.theme
            print("direct",i)
            if(a != None):
                b=a
                a=b
    else:
        b=a
   

    for message in messages:
            if message['user'].username == username:
                message['unread'] = 0
                
    context = {
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
        'profile_receiver':profile_search_selecter,
         'theme':b


    }
    return render(request, 'directs/message.html', context)

def SendDirect(request):
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    print("user_to",to_user_username)
    body = request.POST.get('body')
    checking=request.POST.get('checking')
    msg_id=request.POST.get('msgid')
    #msg_id=int(msg_id)
    print("id",msg_id,'body',body,'checking',checking)
    if(checking=='0'):

        if request.method == "POST":
            to_user = User.objects.get(username=to_user_username)
            Message.sender_message(from_user, to_user, body)
            return redirect('inbox')
    else:
        message=Message.objects.get(id=int(msg_id))
        message.body=body
        message_recepient=Message.objects.get(id=int(msg_id)+1)
        message_recepient.body=body
        message_recepient.save()
        message.save()
        return redirect('inbox')
        

def UserSearch(request):
    query = request.GET.get('q')
    context = {}
    if query:
        users = User.objects.filter(Q(username__icontains=query))

        # Paginator
        paginator = Paginator(users, 8)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)

        context = {
            'users': users_paginator,
            }

    return render(request, 'directs/search.html', context)

def NewConversation(request, username):
    from_user = request.user
    body = ''
    try:
        to_user = User.objects.get(username=username)
    except Exception as e:
        return redirect('usersearch')
    if from_user != to_user:
        Message.sender_message(from_user, to_user, body)
    return redirect('inbox')
def delete_message(request,pk):
    print(type(pk))
    message=Message.objects.get(id=pk)
    message.body='deleting every one'
    message_recepient=Message.objects.get(id=pk+1)
    message_recepient.body='deleting every one'
    message_recepient.save()
    message.save()
    print("message",message)
    return HttpResponsePermanentRedirect(request.META.get('HTTP_REFERER'))

@login_required
def delete_message_for_sender(request, pk):
    message=Message.objects.get(id=pk)
    message.sender_deleted = True
    message.save()
    return HttpResponsePermanentRedirect(request.META.get('HTTP_REFERER'))
@login_required
def delete_message_for_receiver(request, pk):
    message=Message.objects.get(id=pk)
    message.recipient_deleted = True
    message.save()
    return HttpResponsePermanentRedirect(request.META.get('HTTP_REFERER'))

def change_color(request):
    if (request.method == 'POST'):
        user = request.user
        print("inbox",user)
        messages = Message.get_message(user=request.user)
        active_direct = None
        directs = None
        profile = get_object_or_404(Profile, user=user)
        print("profile",profile.user.username)

        if messages:
            message = messages[0]
            active_direct = message['user'].username
            active_user=active_direct
            
            message=Message.objects.filter(reciepient__username=active_user)
            
        set_theme=request.POST.get('theme')
        for i in message:
            i.theme=set_theme
            i.save()
    #return HttpResponsePermanentRedirect(request.META.get('HTTP_REFERER'))
    return redirect('inbox')
    
    
    


    