from django.urls import path
from . import views

urlpatterns = [
    path('/register',views.registration,name='register'),
    path('/login',views.login,name='login'),
    path('/list',views.user_details,name='user_details'), 
    path('/view/<int:id>',views.user_details,name='user_details'),
    path('/change-password', views.change_password, name='change_password'),  
    path('/logout',views.logout,name='logout'),  
]