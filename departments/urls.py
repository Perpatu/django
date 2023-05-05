from django.urls import path
from .views import (
    DepartmentsGetAllView, DepartmentsPostView, DepartmentsToColumnView,
    DepartmentsPutView, DepartmentsDeleteView, DepartmentDetialView,
    AdminCloumnGetView, DepartmentCloumnGetView, DepartmentsGetMainView
)

urlpatterns = [
    path('add/', DepartmentsPostView.as_view()),
    path('get_to_column/', DepartmentsToColumnView.as_view()), 
    path('get_all/', DepartmentsGetAllView.as_view()),   
    path('get_main/', DepartmentsGetMainView.as_view()),
    path('get_admin_column/', AdminCloumnGetView.as_view()),   
    path('get_department_column/<str:dep>/', DepartmentCloumnGetView.as_view()),
    path('update/', DepartmentsPutView.as_view()),
    path('get_detail/<int:pk>/', DepartmentDetialView.as_view()), 
    path('delete/<int:id>/', DepartmentsDeleteView.as_view()), 
]