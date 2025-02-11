from todo.api.v1.views import TaskViewSet
from rest_framework.routers import DefaultRouter


app_name = "api-v1"

router = DefaultRouter()

router.register("todo", TaskViewSet, basename="todo")

urlpatterns = router.urls
