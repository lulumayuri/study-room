from django.urls import URLPattern, path
from . import views
 
urlpatterns  = [
     path('Login/',views.LoginPage,name='Login'),
     path('register/',views.RegisterPage,name='register'),
     path('logout/',views.logoutPage,name='logout'),
     path('',views.Home,name='home'),
     path('Room/<str:pk>/',views.Rooms,name='Room'),
     path('CreateRoom/',views.CreateRoom,name='CreateRoom'),
     path('UpdateRoom/<str:pk>',views.UpdateRoom,name='UpdateRoom'),
     path('DeleteRoom/<str:pk>',views.DeleteRoom,name='DeleteRoom'),
     path('DeleteMessage/<str:pk>/<slug:pk1>',views.DeleteMessage,name='DeleteMessage')
]