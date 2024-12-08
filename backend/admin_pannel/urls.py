from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.Register.as_view(),name='register'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('user/list',views.UserList.as_view()), 
     path('user/view',views.UserView.as_view()),  
    path('logout/',views.LogOutView.as_view()),  
]