from django.urls import path, include
from todo.views import (
    TaskListView,
    TaskCreateView,
    EditTask,
    CompleteTask,
    DeleteTask,
    TaskListApiView,
    CacheWeatherApiView,
)

app_name = "taskApp"
urlpatterns = [
    path("", TaskListView.as_view(), name="task-view"),
    path("todo/api/", TaskListApiView.as_view(), name="task-api-view"),
    path("create", TaskCreateView.as_view(), name="task-create"),
    path("edit/<int:pk>", EditTask.as_view(), name="task-edit"),
    path("complete/<int:pk>", CompleteTask.as_view(), name="task-complete"),
    path("delete/<int:pk>", DeleteTask.as_view(), name="task-delete"),
    path("api/v1/", include("todo.api.v1.urls")),

    # caching (weather api)
    path('todo/weather-api/', CacheWeatherApiView.as_view(), name='weather-api') 

]
