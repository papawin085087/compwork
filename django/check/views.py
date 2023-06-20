from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import CheckIn
from check import serializers


class CheckViewSets(viewsets.ModelViewSet):
    """ View for manage task APIs. """
    serializer_class = serializers.CheckSerializer
    queryset = CheckIn.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        """ Create a new task """
        return serializer.save(user=self.request.user)
