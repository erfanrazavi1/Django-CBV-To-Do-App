from rest_framework import viewsets
from .serializers import TaskSerializer
from ...models import Task
from rest_framework.permissions import IsAuthenticatedOrReadOnly




class TaskModelSerializer(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = TaskSerializer
    queryset = Task.objects.all()