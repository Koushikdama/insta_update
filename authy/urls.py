from django.urls import path
from authy.views import UserProfile, Signup, PasswordChange, PasswordChangeDone, EditProfile,follower_following,handlelogout,token_send,handlelogin,verify,otp_verify

from django.contrib.auth import views as authViews 



urlpatterns = [
   	
    path('profile/edit', EditProfile, name='edit-profile'),
   	path('signup/', Signup, name='signup'),
   	#path('login/', authViews.LoginView.as_view(template_name='login.html'), name='login'),
   	#path('logout/', authViews.LogoutView.as_view(), {'next_page' : 'index'}, name='logout'),
    path('login/', handlelogin, name='login'),
	path('logout/',handlelogout,name='logout'),
   	path('changepassword/', PasswordChange, name='change_password'),
   	path('changepassword/done', PasswordChangeDone, name='change_password_done'),
   	path('passwordreset/', authViews.PasswordResetView.as_view(), name='password_reset'),
   	path('passwordreset/done', authViews.PasswordResetDoneView.as_view(), name='password_reset_done'),
   	path('passwordreset/<uidb64>/<token>/', authViews.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   	path('passwordreset/complete/', authViews.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile/<str:option>/<str:username>',follower_following,name="follower_following"),
    path('token' , token_send , name="token_send"),
    path('verify/<auth_token>' , verify , name="verify"),
    path('otp/verify',otp_verify,name="otp_verify")


]