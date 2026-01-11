from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),             # Accessible at /tasks/
    path('create/', views.task_create, name='task_create'),   # Accessible at /tasks/create/
    path('delete/<int:task_id>/', views.task_delete, name='task_delete'), # Accessible at /tasks/delete/ID/
]