from django.urls import path, include
from rest_framework_nested import routers
from .views import CustomerViewSet, InteractionViewSet, CustomerProjectViewSet

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet,basename='customer')

customers_router = routers.NestedSimpleRouter(router, r'customers', lookup='customer')
customers_router.register(r'interactions', InteractionViewSet, basename='customer-interactions')
customers_router.register(r'projects', CustomerProjectViewSet, basename='customer-projects')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(customers_router.urls)),
    path('customers/<int:pk>/upload_image/', 
         CustomerViewSet.as_view({'post': 'upload_image'}), 
         name='customer-upload-image'),
]