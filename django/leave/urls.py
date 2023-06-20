from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter
from leave import views

router = DefaultRouter()

router.register('leaves', views.EventViewSets)

app_name = 'leave'

urlpatterns = [
    path('', include(router.urls)),
]
