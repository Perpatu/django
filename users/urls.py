from django.urls import path, re_path
from rest_framework.authtoken.views import obtain_auth_token 
from .views import (
    RegisterView, LoginView, LogoutView,
    AdminChangePasswordView, UserChangePasswordView,
    UserGetCurrentView, UserChangeView, UserDeleteView,
    UsersGetAllView, UserAdminView, UserNotAdminView,   
    UserDetailView,    
)


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('logout/', LogoutView.as_view()),
    path('get_current/', UserGetCurrentView.as_view()),
    path('get_detail/<int:pk>/', UserDetailView.as_view()),
    path('get_all/', UsersGetAllView.as_view()),
    path('get_admin/', UserAdminView.as_view()),
    path('get_not_admin/', UserNotAdminView.as_view()),
    path('update/', UserChangeView.as_view()),
    path('delete/<int:id>/', UserDeleteView.as_view()),
    path('change_admin_password/', AdminChangePasswordView.as_view()),
    path('change_password/', UserChangePasswordView.as_view()),  
]