from django.urls import path
from Messages.views import inbox, UserSearch, Directs, NewConversation, SendDirect,delete_message,delete_message_for_sender,delete_message_for_receiver,change_color
urlpatterns = [
   	path('', inbox, name='inbox'),
   	path('directs/<username>', Directs, name='directs'),
   	path('/new/', UserSearch, name='usersearch'),
   	path('new/<username>', NewConversation, name='newconversation'),
    path('/send/', SendDirect, name="send-directs"),
    path('delete-message/<int:pk>',delete_message,name='delete-message'),
    path('delete-message-for/<int:pk>',delete_message_for_sender,name='delete-for-me'),
    path('delete-receive-meg/<int:pk>',delete_message_for_receiver,name='delete-receiver-msg'),
    path('/change-theme/', change_color, name='change-color')


   
    

]