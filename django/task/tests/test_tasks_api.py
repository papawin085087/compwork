"""
Tests for tasks APIs.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Task
from task.serializers import (
    TaskSerializer,
    # TaskDetailSerializer,
)

TASK_URL = reverse('task:task-list')


def detai_url(task_id):
    return reverse('task:task-detail', args=[task_id])


def create_task(user, **params):
    """ Create and return a sample task. """
    defaults = {
        'title': 'Test title',
        'content': 'Test content',
    }

    defaults.update(params)

    task = Task.objects.create(user=user, **defaults)

    return task


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicTaskAPITests(TestCase):
    """ Test unauthenticated API request. """

    def setUp(self):

        self.client = APIClient()

    def test_auth_required(self):
        """ Test auth is required to call API. """
        res = self.client.get(TASK_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTaskAPITests(TestCase):
    """ Test authenticated is request. """

    def setUp(self):

        self.client = APIClient()
        self.user = create_user(email='test@teset.com', password='test123')
        self.client.force_authenticate(self.user)

    def test_retrive_task(self):
        """ Test retrieving a list of task. """
        create_task(user=self.user)
        create_task(user=self.user)

        res = self.client.get(TASK_URL)

        task = Task.objects.all().order_by('-id')

        serializer = TaskSerializer(task, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_task_list_limited_to_user(self):
        """ Test list of task is limited to authenticated user. """
        other_user = create_user(email='other@other.com', password='other123')
        create_task(user=other_user)
        create_task(user=self.user)

        res = self.client.get(TASK_URL)

        task = Task.objects.filter(user=self.user)

        serializer = TaskSerializer(task, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # def test_get_task_content(self):
    #     """ Test get task content """
    #     task = create_task(user=self.user)

    #     url = detai_url(task.id)

    #     res = self.client.get(url)

    #     serializer = TaskDetailSerializer(task)

    #     self.assertEqual(res.data, serializer.data)

    def test_create_task(self):
        """ Test creating a task """
        payload = {
            'title': 'test title',
            'content': 'test content',
        }

        res = self.client.post(TASK_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        task = Task.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(task, k), v)
        self.assertEqual(task.user, self.user)

    def test_partial_update(self):
        """ Test partial update of a task """
        original_content = 'original content'
        task = create_task(
            user=self.user,
            title='Test title',
            content=original_content,
        )

        payload = {'title': 'New title update'}

        url = detai_url(task.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, payload['title'])
        self.assertEqual(task.content, original_content)
        self.assertEqual(task.user, self.user)

    def test_full_update(self):
        """ Test full update of task. """
        task = create_task(
            user=self.user,
            title='Test title',
            content='Test Content',
        )

        payload = {
            'title': 'New title',
            'content': 'New content'
        }

        url = detai_url(task.id)

        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(task, k), v)
        self.assertEqual(task.user, self.user)

    def test_update_user_returns_error(self):
        """ Test changing the task user result in an error. """
        new_user = create_user(email='new@new.com', password='new123')

        task = create_task(user=self.user)

        payload = {'user': new_user.id}

        url = detai_url(task.id)

        self.client.patch(url, payload)

        task.refresh_from_db()

        self.assertEqual(task.user, self.user)

    def test_delete_task(self):
        """ Test deleting a task successfull. """
        task = create_task(user=self.user)

        url = detai_url(task.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_delete_other_user_task_error(self):
        """ Test trying to delete another user task give error. """
        new_user = create_user(email='new@new.com', password='new123')

        task = create_task(user=new_user)

        url = detai_url(task.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Task.objects.filter(id=task.id).exists())
