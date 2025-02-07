from rest_framework import serializers
from ...models import Task, User


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = [
            "id",
            "user",
            "title",
            "complete",
            "created_date",
            "updated_date",
        ]
        read_only_fields = ["user"]

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     return representation

    def create(self, validated_data):
        validated_data["user"] = User.objects.get(
            id=self.context.get("request").user.id
        )
        return super().create(validated_data)
