from django.shortcuts import render, redirect, get_object_or_404
from authy.forms import SignupForm, ChangePasswordForm, EditProfileForm
from django.contrib.auth.models import User
from Post.models import Stream,Post,Follow
from django.contrib.auth import authenticate,login,logout
from django.core.mail import message
import os
from django.db import transaction
from django.urls import reverse
from django.urls import resolve
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse, HttpResponseRedirect
from authy.models import Profile
from django.template import loader
from django.http import HttpResponse
from authy.sendmail import sendmail

from django.core.paginator import Paginator
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
import random
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
from django.contrib import messages
otp_otp= ''.join([str(random.randint(0, 9)) for _ in range(6)])
auth_token=""
# Create your views here.
def UserProfile(request, username):
	if(request.user.username == username):
		
		user = get_object_or_404(User, username=username)
		profile = Profile.objects.get(user=user)
		url_name = resolve(request.path).url_name
		if url_name == 'profile':
			posts = Post.objects.filter(user=user).order_by('-posted')
		else:
			posts = profile.favorites.all()
		#Profile info box
		posts_count = Post.objects.filter(user=user).count()
		following_count = Follow.objects.filter(follower=user).count()
		followers_count = Follow.objects.filter(following=user).count()
		#follow status
		follow_status = Follow.objects.filter(following=user, follower=request.user).exists()
		#Pagination
		paginator = Paginator(posts, 8)
		page_number = request.GET.get('page')
		posts_paginator = paginator.get_page(page_number)

		template = loader.get_template('profile/profile.html')

		context = {
			'posts': posts_paginator,
			'profile':profile,
			'following_count':following_count,
			'followers_count':followers_count,
			'posts_count':posts_count,
			'follow_status':follow_status,
			'url_name':url_name,
			'account_status':'login_user'
			
		}

		return HttpResponse(template.render(context, request))
	else:
		list_login_following=[]
		list_login_follower=[]
		list_search_following=[]
		list_search_follower=[]
		login_follower_following=[]
		
		user = get_object_or_404(User, username=username)
		profile = Profile.objects.get(user=user)

	####################private###########################
		if(profile.is_private == 'private'):
			log_user = get_object_or_404(User, username=request.user.username)	
			login_following=Follow.objects.filter(following = log_user)
			for i in login_following:
				list_login_following.append(i.follower.username)

			login_follower=Follow.objects.filter(follower=log_user)
			for i in login_follower:
				list_login_follower.append(i.following.username)
			
			login_follower_following.append(set(list_login_follower) and set(list_login_following))
			#print(login_follower_following)

			search_user = get_object_or_404(User, username=username)
			search_following=Follow.objects.filter(following = search_user)
			for i in search_following:
				list_search_following.append(i.follower.username)

			search_follower=Follow.objects.filter(follower=search_user)
			for i in search_follower:
				list_search_follower.append(i.following.username)
			search_follower_following=(set(list_search_following) and set(list_search_follower))
			login_follower_following=(set(list_login_following) and set(list_login_follower))
			
			####################check_both_follower_following both are in friends ###########################
			if(str(log_user) in search_follower_following and str(search_user) in login_follower_following):
				url_name = resolve(request.path).url_name
				if url_name == 'profile':
					posts = Post.objects.filter(user=user).order_by('-posted')
				else:
						posts = profile.favorites.all()
				#Profile info box
				posts_count = Post.objects.filter(user=user).count()
				following_count = Follow.objects.filter(follower=user).count()
				followers_count = Follow.objects.filter(following=user).count()
				#follow status
				follow_status = Follow.objects.filter(following=user, follower=request.user).exists()
				#Pagination
				paginator = Paginator(posts, 8)
				page_number = request.GET.get('page')
				posts_paginator = paginator.get_page(page_number)
				#print("private_public")

				template = loader.get_template('profile/private_public.html')

				context = {
				'posts': posts_paginator,
				'profile':profile,
				'following_count':following_count,
				'followers_count':followers_count,
				'posts_count':posts_count,
				'follow_status':follow_status,
				'url_name':url_name,
				"user_name":str(search_user),
				'account_status':"private_public"
					}

				return HttpResponse(template.render(context, request))
			#################private without friends ###########################	
			else:
				url_name = resolve(request.path).url_name
				if url_name == 'profile':
					posts = Post.objects.filter(user=user).order_by('-posted')
				else:
						posts = profile.favorites.all()
				#Profile info box
				posts_count = Post.objects.filter(user=user).count()
				following_count = Follow.objects.filter(follower=user).count()
				followers_count = Follow.objects.filter(following=user).count()
				#follow status
				follow_status = Follow.objects.filter(following=user, follower=request.user).exists()
				#Pagination
				paginator = Paginator(posts, 8)
				page_number = request.GET.get('page')
				posts_paginator = paginator.get_page(page_number)
				#print("private_public")

				template = loader.get_template('profile/private_public.html')

				context = {
				'posts': posts_paginator,
				'profile':profile,
				'following_count':following_count,
				'followers_count':followers_count,
				'posts_count':posts_count,
				'follow_status':follow_status,
				'url_name':url_name,
				"user_name":str(search_user),
				'account_status':"private"
					}

				return HttpResponse(template.render(context, request))
			#################public###########################
		else:
			url_name = resolve(request.path).url_name
			if url_name == 'profile':
				posts = Post.objects.filter(user=user).order_by('-posted')
			else:
				posts = profile.favorites.all()
			#Profile info box
			posts_count = Post.objects.filter(user=user).count()
			following_count = Follow.objects.filter(follower=user).count()
			followers_count = Follow.objects.filter(following=user).count()
			#follow status
			follow_status = Follow.objects.filter(following=user, follower=request.user).exists()
			#Pagination
			paginator = Paginator(posts, 8)
			page_number = request.GET.get('page')
			posts_paginator = paginator.get_page(page_number)

			template = loader.get_template('profile/private_public.html')
			print("puublic",profile.user.username)

			context = {
			'posts': posts_paginator,
			'profile':profile,
			'following_count':following_count,
			'followers_count':followers_count,
			'posts_count':posts_count,
			'follow_status':follow_status,
			'url_name':url_name,
			'user_name'    :username,
			'account_status':"public"
		}

			return HttpResponse(template.render(context, request))

		
		

def Signup(request):
	if request.method == 'POST':
		
		form = SignupForm(request.POST)
		if form.is_valid():
			print("invalid")
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
            
			user_obj = User(username = username , email = email)
			user_obj.set_password(password)
			user_obj.save()
			global auth_token
			auth_token = str(uuid.uuid4())
			print("auth_token",type(auth_token))
			print("otp",otp_otp)
			
			

			profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token)
			profile_obj.save()
			
			send_mail_after_registration(email , auth_token,otp_otp)
			
			
			return redirect('/user/token')
		else:
			return redirect('signup')

            
	else:
		form = SignupForm()
	context = {
		'form':form,
	}
    
	return render(request,'signup.html',context)


@login_required
def PasswordChange(request):
	user = request.user
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			new_password = form.cleaned_data.get('new_password')
			user.set_password(new_password)
			user.save()
			update_session_auth_hash(request, user)
			return redirect('change_password_done')
	else:
		form = ChangePasswordForm(instance=user)
		profile=Profile()

	context = {
		'form':form,
	}

	return render(request, 'change_password.html', context)

def PasswordChangeDone(request):
	return render(request, 'change_password_done.html')


@login_required
def EditProfile(request):		
	user = request.user.id
	profile = Profile.objects.get(user__id=user)
	before_img_update=profile.picture
	
	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES)
		if form.is_valid():
			
			#profile = Profile.objects.get(user__id=user)
			
			profile.picture = form.cleaned_data.get('picture')
			#profile = Profile.objects.get(user__id=user)
		
			if(profile.picture):
				profile.picture = form.cleaned_data.get('picture')
			else:
				profile.picture=before_img_update
				
			profile.first_name = form.cleaned_data.get('first_name')
			profile.last_name = form.cleaned_data.get('last_name')
			profile.location = form.cleaned_data.get('location')
			profile.url = form.cleaned_data.get('url')
			profile.profile_info = form.cleaned_data.get('profile_info')
			profile.is_private=form.cleaned_data.get('type_account')
			profile.is_send_notifications=form.cleaned_data.get('send_mail')
			profile.save()
			return redirect('index')
			
	else:
		form = EditProfileForm()
		print("else",profile.picture)
		
		
		
		user = request.user.id
		profile = Profile.objects.get(user__id=user)
		
		
		
	context = {
		'form':form,
		'profile':profile,
		"profile_type":profile.is_private,
		"profile_sms":profile.is_send_notifications,
		"previouspic":profile.picture
	}

	return render(request, 'edit_profile.html', context)


@login_required
def follow(request, username, option):
	following = get_object_or_404(User, username=username)
	print("follow",username)
	print("login",request.user)
	try:
		f, created = Follow.objects.get_or_create(follower=request.user, following=following)
		if int(option) == 0:
			f.delete()
   #getting email useing username  
			sender=get_object_or_404(User, username=username)
			sender_email=sender.email
   # getting profile object using username 
			user_id=User.objects.get(username=username)
			receiver_user=get_object_or_404(Profile, user=user_id)
			if(receiver_user.is_send_notifications== 'yes'):
				sendmail(sender_email,username,0,request.user)

			Stream.objects.filter(following=following, user=request.user).all().delete()
		else:
			posts = Post.objects.all().filter(user=following)[:25]

			with transaction.atomic():
				for post in posts:
					stream=Stream(post=post,user=request.user,date=post.posted,following=following)
					stream.save()
		sender=get_object_or_404(User, username=username)
		sender_email=sender.email
		print("sender_email",sender_email)
			#getting email useing username  
		sender=get_object_or_404(User, username=username)
		sender_email=sender.email
   				# getting profile object using username 
		user_id=User.objects.get(username=username)
		receiver_user=get_object_or_404(Profile, user=user_id)
		if(receiver_user.is_send_notifications== 'yes'):
			sendmail(sender_email,username,1,request.user)

		return HttpResponseRedirect(reverse('profile', args=[username]))
				
	except User.DoesNotExist:
		return HttpResponseRedirect(reverse('profile', args=[username]))

@login_required
# function will check following and follower users 
def follower_following(request,option,username):
	user = get_object_or_404(User, username=request.user)
	login_profile = Profile.objects.get(user=user)
	if(option == 'following' ):	
		post_number=[]
		followers_number=[]
		following_number=[]
		profile_following=[]

		#username=request.user.username
		user = get_object_or_404(User, username=username)
		followings=Follow.objects.filter(follower=user)
		for i in followings:
			user = get_object_or_404(User, username=i.following.username)
			profile = Profile.objects.get(user=user)
			profile_following.append(profile)
			posts_count = Post.objects.filter(user=user).count()
			post_number.append(posts_count)
			following_no = Follow.objects.filter(follower=user).count()
			following_number.append(following_no)
			#print("following",Follow.objects.filter(follower=user))
			followers_no = Follow.objects.filter(following=user).count()
			followers_number.append(followers_no)
		following_details=zip(profile_following,post_number,following_number,followers_number)
		print("if",type(username))
		print("if",type(str(login_profile)))
		context={
			'follow':following_details,
			'option':option,
			'profile':str(login_profile),
			'username':username
		}
		return render(request,"followandfollowing.html",context)
			
	else:
		post_number=[]
		followers_number=[]
		following_number=[]
		profile_following=[]
		#username=request.user.username
		user = get_object_or_404(User, username=username)
		followers=Follow.objects.filter(following=user)
		for i in followers:
			user = get_object_or_404(User, username=i.follower.username)
			profile = Profile.objects.get(user=user)
			profile_following.append(profile)
			print("USER :",user)
			posts_count = Post.objects.filter(user=user).count()
			post_number.append(posts_count)
			following_no = Follow.objects.filter(follower=user).count()
			following_number.append(following_no)
			#print("following",Follow.objects.filter(follower=user))
			followers_no = Follow.objects.filter(following=user).count()
			followers_number.append(followers_no)
			print("postcount",posts_count,"following_count",following_no,"follower_count",followers_no)
		following_details=zip(profile_following,post_number,following_number,followers_number)
		print("else",type(username))
		print("else",type(login_profile))
		context={
			'follow':following_details,
			'option':option,
			'profile':str(login_profile),
			'username':username
   
			
		}
		return render(request,"followandfollowing.html",context)
		
	
	
	

		    
	







"""
	followings=Follow.objects.filter(follower=user)
	for i in followings:
		print("using followering",i.following.username)
	follower=[]
	followersi=Follow.objects.filter(follower=user)
	for i in followersi:
		follower.append(i.follower.username)
		print("using followers",i.follower.username)
	print(follower)
		"""
def handlelogout(request):
    logout(request)
    
    return redirect('login')



def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('login')
        else:
            return HttpResponse("error2")

    except Exception as e:
        print(e)
        return redirect('/')
def send_mail_after_registration(email , token,otp):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token} or verify using otp your otp is:{otp}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )
def token_send(request):
    return render(request , 'token_send.html')


def otp_verify(request):
    
    
    print("original",otp_otp)
    o_t_p = request.GET.get('o_t_p','')
    print("otp_form",type(o_t_p))
    print("auth_token",type(auth_token))
    print(len(str(o_t_p)) == 6)
   
    if(len(str(o_t_p)) == 6):
        if(int(o_t_p)==int(otp_otp)):
            try:
                profile_obj = Profile.objects.filter(auth_token = auth_token).first()
                if profile_obj:
            	    if profile_obj.is_verified:
                		messages.success(request, 'Your account is already verified.')
                		return redirect('login')
            	    profile_obj.is_verified = True
            	    profile_obj.save()
            	    messages.success(request, 'Your account has been verified.')
            	    return redirect('login')
                else:
            	    return HttpResponse("error2")
            except Exception as e:
                print(e)
            
        else:
            messages.error(request, 'WORNG OTP')
            return redirect('token_send')
            
            
    else:
        messages.error(request, 'INVALID OTP')
        return redirect('token_send')
        
    










def handlelogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('login')
        
        
        profile_obj = Profile.objects.filter(user = user_obj ).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('login')

        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('login')
        
        login(request , user)
        #return redirect('/')
        return redirect("index")

    return render(request , 'login.html')







