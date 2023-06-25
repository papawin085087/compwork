from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Event
from leave import serializers


class EventViewSets(viewsets.ModelViewSet):
    """ View for manage task APIs. """
    serializer_class = serializers.EventSerializer
    queryset = Event.objects.all()
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     if self.request.user.is_superuser == True:
    #         return self.queryset
    #     return self.queryset.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        """ Create a new task """
        return serializer.save(user=self.request.user)
