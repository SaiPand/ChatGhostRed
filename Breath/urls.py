from django.urls import path
from . import views

app_name = 'algo'
urlpatterns = [
    path('', views.iniciarseccion,name='login'),
    path('logout/', views.cerraseccion,name='logout'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('<str:room>/', views.room, name='room'),
    path('chat/<str:room>/<str:user>', views.room2, name='room2'),
    path('home/checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('deleteRoom/<str:room>/', views.roomDelete, name='deleteRoom'),
    path('editRoom/<str:room>/', views.editroom, name='edit')
]