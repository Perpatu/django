from django.urls import path
from .views import QueueFilePostView, QueueFileGetView, QueueDeleteView, FilesPutView

urlpatterns = [
    path('add/<int:project_id>/', QueueFilePostView.as_view()),
    path('get/', QueueFileGetView.as_view()),
    path('update/<int:project_id>/', FilesPutView.as_view()),
    path('delete/<int:id>/<int:project_id>/', QueueDeleteView.as_view()),
]