from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from taskapp.views import TaskViewSet

router = DefaultRouter()
router.register(r'api/tasks', TaskViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]