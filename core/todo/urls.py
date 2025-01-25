from django.urls import path , include
from .views import *
app_name  = 'taskApp'

urlpatterns = [
    path('' , TaskListView.as_view() , name ='task-view'),
    path('create' , TaskCreateView.as_view() , name ='task-create'),
    path('edit/<int:pk>' , EditTask.as_view() , name ='task-edit'),
    path('complete/<int:pk>' , CompleteTask.as_view() , name ='task-complete'),
    path('delete/<int:pk>' , DeleteTask.as_view() , name ='task-delete'),
    path('api/v1/' , include('todo.api.v1.urls'))
]

