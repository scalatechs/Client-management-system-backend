from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ComplaintViewSet

router = DefaultRouter()
router.register(r'complaints', ComplaintViewSet, basename='complaint')

urlpatterns = [
    path('', include(router.urls)),
    path('complaints/<int:pk>/update_status/', 
         ComplaintViewSet.as_view({'post': 'update_status'}), 
         name='update-complaint-status'),
]