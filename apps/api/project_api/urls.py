from django.urls import path, include
from rest_framework_nested import routers
from .views import ProjectViewSet, MilestoneViewSet

router = routers.DefaultRouter()
router.register(r'', ProjectViewSet, basename='project')

projects_router = routers.NestedSimpleRouter(router, r'', lookup='project')
projects_router.register(r'milestones', MilestoneViewSet, basename='project-milestones')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(projects_router.urls)),
    path('<int:pk>/add_employee/', 
         ProjectViewSet.as_view({'post': 'add_employee'}), 
         name='project-add-employee'),
]