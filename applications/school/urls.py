from django.urls import path, include
from rest_framework.routers import DefaultRouter
from applications.school.views import SchoolViewSet

router = DefaultRouter()
router.register(r'', SchoolViewSet)

urlpatterns = [
    path('', include(router.urls)),
]