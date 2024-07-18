"""instagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from authy.views import UserProfile,follow
urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include('authy.urls')),
   path('post/',include('Post.urls')),
    path('<username>/', UserProfile, name='profile'),
    path('<username>/saved', UserProfile, name='profilefavorites'),
    path('<username>/follow/<option>', follow, name='follow'),
    path('message', include('Messages.urls')),
    path('notifications/', include('Notifications.urls')),
    path('stories/', include('Stories.urls')),
    #path('active/(?p<uidb64>[0-9A-Za-Z_\-]+)/(?p<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',vi)
    #path('verification/', include('verify_email.urls')),	

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
