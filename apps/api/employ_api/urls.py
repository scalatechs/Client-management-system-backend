from django.urls import path, include
from rest_framework_nested import routers
from .views import EmployeeViewSet, ContractViewSet, EmployeeProjectAssignmentViewSet

router = routers.DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')

employees_router = routers.NestedSimpleRouter(router, r'employees', lookup='employee')
employees_router.register(r'contracts', ContractViewSet, basename='contract')
employees_router.register(r'assignments', EmployeeProjectAssignmentViewSet, basename='assignment')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(employees_router.urls)),
]