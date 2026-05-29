from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, MessageViewSet, AnnouncementViewSet

router = DefaultRouter()
router.register('rooms', RoomViewSet, basename='rooms')
router.register('messages', MessageViewSet, basename='messages')
router.register('announcements', AnnouncementViewSet, basename='announcements')

urlpatterns = [
    path('', include(router.urls)),
]
