from rest_framework import serializers
from core.models import Event


class EventSerializer(serializers.ModelSerializer):

    owner_name = serializers.CharField(source='user.name', required=False)
    owner_lname = serializers.CharField(source='user.l_name', required=False)
    owner_email = serializers.EmailField(source='user.email', required=False)
    owner_employee = serializers.CharField(source='user.employee_type', required=False)
    owner_team = serializers.CharField(source='user.team', required=False)

    class Meta:
        model = Event
        fields = ['id', 'user',  'owner_name', 'owner_lname', 'owner_email', 'owner_employee', 'owner_team', 'event_title', 'event_description',
                  'event_status', 'event_type', 'event_date', 'event_end']
        read_only_fields = ['id', 'user', 'owner_name', 'owner_lname', 'owner_email', 'owner_employee', 'owner_team']
