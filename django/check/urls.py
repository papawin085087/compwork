from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter
from check import views

router = DefaultRouter()

router.register('', views.CheckViewSets)

app_name = 'check'

urlpatterns = [
    path('', include(router.urls)),
]
