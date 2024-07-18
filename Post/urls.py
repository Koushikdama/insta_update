from django.urls import path
from Post.views import index,NewPost,PostDetails,tags,like,favorite,search_user

urlpatterns = [


    path('',index,name='index'),
    path('newpost/',NewPost,name='newpost'),
   
    path('tag/<slug:tag_slug>', tags, name='tags'),
   # path('<uuid:post_id>/like', like, name='postlike'),
   path('<uuid:post_id>/like', like, name='postlike'),
    path('<uuid:post_id>/favorite', favorite, name='postfavorite'),
     path('<uuid:post_id>', PostDetails, name='postdetails'),
     path('<str:search_user>/search',search_user,name="search")
    

]