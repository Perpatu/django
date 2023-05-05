from django.urls import path
from .views import (
    ProjectPostView, ProjectPutView, ProjectDetialView,
    ProjectDeleteView, ProjectActiveView, ProjectCompletedView,
    ProjectPausedView, ProjectUserCompletedView , ProjectUserCompletedView,
    ProjectUserActiveView, ProjectSecretariatActiveView, ProjectSecretariatCompletedView,
    ProjectActiveClientView, ProjectCompletedClientView, ProjectActiveCalendarView,
    ProjectActiveClientBoardView, ProjectActiveClientBoardSecretariatView
)

urlpatterns = [
    path('add/', ProjectPostView.as_view()),
    path('update/', ProjectPutView.as_view()),
    path('delete/<int:id>/', ProjectDeleteView.as_view()),
    path('get_detail/<int:pk>/', ProjectDetialView.as_view()),
    path('get_all_active/', ProjectActiveView.as_view()),
    path('get_all_completed/', ProjectCompletedView.as_view()),
    path('get_all_paused/', ProjectPausedView.as_view()),
    path('get_project_calendar/', ProjectActiveCalendarView.as_view()),
    path('get_user_active/<int:User_id>/', ProjectUserActiveView.as_view()),
    path('get_user_completed/<int:User_id>/', ProjectUserCompletedView.as_view()),
    path('get_secretariat_active/', ProjectSecretariatActiveView.as_view()),
    path('get_secretariat_completed/', ProjectSecretariatCompletedView.as_view()),
    path('get_projects_client_sorted/', ProjectActiveClientBoardView.as_view()),
    path('get_projects_client_sorted_secretariat/', ProjectActiveClientBoardSecretariatView.as_view()),
    path('get_client_active_projects/<str:client>/', ProjectActiveClientView.as_view()),
    path('get_client_completed_projects/<str:client>/', ProjectCompletedClientView.as_view()),
]