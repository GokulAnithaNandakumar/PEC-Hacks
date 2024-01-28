from django.urls import path
from . import views

urlpatterns = [
    path('',views.homePage ,  name = "homePage"),
    path('helper/' , views.helperPage ,  name = "helperPage"),
    path('user/' , views.userPage , name = "userPage"),
    path('callback/', views.callback, name='callback'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    

    # User 
    path('send_message/', views.send_message, name='send_message'),
    path('get_chat_history/', views.get_chat_history, name='get_chat_history'),
    
    # Helper
    path('get_chat_history_for_user/', views.get_chat_history_for_user, name='get_chat_history_for_user'),
    path('send_reply/', views.send_reply, name='send_reply'),
    path('get_users/' , views.get_users, name='get_users'),
    
]
