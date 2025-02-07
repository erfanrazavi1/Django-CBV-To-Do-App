from todo.api.v1.views import TaskModelSerializer
from rest_framework.routers import DefaultRouter


app_name = "api-v1"

router = DefaultRouter()

router.register("todo", TaskModelSerializer, basename="todo")

urlpatterns = router.urls
