import pytest
from django.contrib.auth.models import User
from todo.models import Task
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """Provides an API client for testing API requests."""
    return APIClient()


@pytest.fixture
def test_user():
    """Creates and returns a test user."""
    return User.objects.create(username="erf1", password="123")


@pytest.fixture
def task_factory():
    """Factory fixture to create task instances dynamically."""

    def create_task(user, title="Test Test", complete=False):
        return Task.objects.create(user=user, title=title, complete=complete)

    return create_task
