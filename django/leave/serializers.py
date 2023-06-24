from rest_framework import serializers
from core.models import Event


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['id', 'user', 'event_title', 'event_description',
                  'event_status', 'event_type', 'event_date', 'event_end']
        read_only_fields = ['id', 'user', 'event_status']
