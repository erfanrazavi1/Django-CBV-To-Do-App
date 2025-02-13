from django.urls import reverse
import pytest


@pytest.mark.django_db
class TestTodoList:

    def test_get_list(self, api_client, test_user, task_factory):
        api_client.force_authenticate(user=test_user)
        """Tests if the API correctly retrieves the list of tasks."""
        task_factory(user=test_user, title="Task 1", complete=False)
        task_factory(user=test_user, title="Task 2", complete=True)
        url = reverse("taskApp:api-v1:todo-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_get_task_detail(self, api_client, test_user, task_factory):
        api_client.force_authenticate(user=test_user)
        """Tests if the API correctly retrieves a single task's details."""
        task = task_factory(
            user=test_user, title="Task Detail", complete=False
        )
        url = reverse("taskApp:api-v1:todo-detail", kwargs={"pk": task.id})
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_task(self, api_client, test_user):
        """Tests if the API allows an authenticated user to create a new task."""
        api_client.force_authenticate(user=test_user)
        url = reverse("taskApp:api-v1:todo-list")
        data = {"user": test_user.id, "title": "new task", "complete": False}
        response = api_client.post(url, data, format="json")
        assert response.status_code == 201
        assert response.data["title"] == "new task"
        assert response.data["complete"] is False

    def test_update_task(self, api_client, test_user, task_factory):
        """Tests if an authenticated user can update an existing task."""
        api_client.force_authenticate(user=test_user)
        task = task_factory(
            user=test_user, title="Task Detail", complete=False
        )
        url = reverse("taskApp:api-v1:todo-detail", kwargs={"pk": task.id})
        data = {
            "user": test_user.id,
            "title": "Updated Task",
            "complete": True,
        }
        response = api_client.put(url, data, format="json")
        assert response.status_code == 200
        assert response.data["title"] == "Updated Task"
        assert response.data["complete"] is True

    def test_delete_task(self, api_client, test_user, task_factory):
        """Tests if an authenticated user can delete a task."""
        api_client.force_authenticate(user=test_user)
        task = task_factory(
            user=test_user, title="Task to Delete", complete=False
        )
        url = reverse("taskApp:api-v1:todo-detail", kwargs={"pk": task.id})
        response = api_client.delete(url)
        assert response.status_code == 204
