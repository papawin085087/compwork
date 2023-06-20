from rest_framework import serializers
from core.models import CheckIn


class CheckSerializer(serializers.ModelSerializer):

    class Meta:
        model = CheckIn
        fields = ['id', 'check_status', 'check_in_time', 'check_out_time']
        read_only_fields = ['id']
