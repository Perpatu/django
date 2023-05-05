from django.urls import path
from .views import (
    FileUploadView, FilesPutView, FilesDeleteView,
    FileProjectGetView, FileSecretariatGetView, FileShopGetView,
    FileDetialView, FileProjectAdminGetView, DownloadView,
    FilesDepartmentsGetView, FilesNumberDepartment,
    FileUploadInquiryView, FilesInquiryGetView,
    FilesInquiryDeleteView, DownloadInquiryView
    
)


urlpatterns = [
    path('upload/<int:project_id>/', FileUploadView.as_view(), name='file-upload'),
    path('upload_inquiry/', FileUploadInquiryView.as_view(), name='file-upload-inquiry'),
    path('update/<int:project_id>/', FilesPutView.as_view()),
    path('get_detail/<int:pk>/', FileDetialView.as_view()),
    path('delete/<int:id>/<int:project_id>/', FilesDeleteView.as_view()),
    path('delete_inquiry/<int:id>/', FilesInquiryDeleteView.as_view()),
    path('get_files_production/<int:project_id>/', FileProjectGetView.as_view()),
    path('get_file_admin/<int:project_id>/', FileProjectAdminGetView.as_view()),
    path('get_files_project_secretariat/<int:project_id>/', FileSecretariatGetView.as_view()),
    path('get_files_inquiry/<int:id>/', FilesInquiryGetView.as_view()),
    path('get_files_project_shop/<int:project_id>/', FileShopGetView.as_view()),   
    path('get_department_files/<str:dep>/', FilesDepartmentsGetView.as_view()),    
    path('number_department_files/<str:dep>/', FilesNumberDepartment.as_view()), 
    path('download/<int:id>/', DownloadView.as_view(), name='download'),
    path('download_inquiry/<int:id>/', DownloadInquiryView.as_view(), name='download_inquiry')

]