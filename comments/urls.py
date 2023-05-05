from django.urls import path
from .views import (
    FileCommentsPostView, ComentFileDeleteView,
    ProjectCommentsPostView, ComentProjectDeleteView
) 

urlpatterns = [
    path('add_file/<int:project_id>/', FileCommentsPostView.as_view()),
    path('add_project/<int:project_id>/', ProjectCommentsPostView.as_view()),
    path('delete_file/<int:id>/<int:project_id>/', ComentFileDeleteView.as_view()),
    path('delete_project/<int:id>/<int:project_id>/', ComentProjectDeleteView.as_view()),
]