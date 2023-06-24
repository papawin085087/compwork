"""
Serializer for task APIs.
"""

from rest_framework import serializers
from core.models import Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'content', 'date_start',
                  'time_start', 'date_end', 'time_end']
        read_only_fields = ['id', 'user', 'date_start', 'time_start']
