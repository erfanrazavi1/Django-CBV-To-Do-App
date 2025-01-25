from rest_framework import viewsets
from .serializers import TaskSerializer
from ...models import Task



class TaskModelSerializer(viewsets.ModelViewSet):
    
    serializer_class = TaskSerializer
    queryset = Task.objects.all()