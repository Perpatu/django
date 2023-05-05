from django.urls import path

from .views import (
    InquiryPostView, InquiryGetNewView, InquiryDetialView,
    InquiryDeleteView, InquiryPutView, InquiryAcceptedView,
    InquiryRejectedView, InquiryConsiderationView,
    InquiryGetNewQuantityView
)

urlpatterns = [
    path('add/', InquiryPostView.as_view()),
    path('update/', InquiryPutView.as_view()),
    path('get_new/', InquiryGetNewView.as_view()),
    path('get_accepted/', InquiryAcceptedView.as_view()),
    path('get_rejected/', InquiryRejectedView.as_view()),
    path('get_consideration/', InquiryConsiderationView.as_view()),
    path('get_new_quantity/', InquiryGetNewQuantityView.as_view()),
    path('get_detail/<int:pk>/', InquiryDetialView.as_view()),
    path('delete/<int:id>/', InquiryDeleteView.as_view()),
]