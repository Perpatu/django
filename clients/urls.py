from django.urls import path, re_path
from .views import (
    ClientPostView, ClientGetView, 
    ClientDatailView, ClientPutView,
    ClientDeleteView   
)

urlpatterns = [
    path('add/', ClientPostView.as_view()),
    path('get_all/', ClientGetView.as_view()),    
    re_path(r'^get_deatil/([0-9]+)/$', ClientDatailView.as_view()), 
    path('update/', ClientPutView.as_view()), 
    path('delete/<int:id>/', ClientDeleteView.as_view()),
]