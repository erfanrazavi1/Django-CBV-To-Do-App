from rest_framework import serializers
from ...models import Task

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['user' , 'title' , 'complete' , 'created_date' , 'updated_date']