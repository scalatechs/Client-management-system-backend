from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.projects.models import Project, Milestone
from .serializers import ProjectSerializer, MilestoneSerializer
from .permissions import IsManagerOrAdmin

class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]

    def get_queryset(self):
        return Project.objects.select_related('manager', 'customer')\
            .prefetch_related('employees', 'milestones')\
            .order_by('-created_at')

    @action(detail=True, methods=['post'])
    def add_employee(self, request, pk=None):
        project = self.get_object()
        employee_id = request.data.get('employee_id')
        try:
            employee = Employee.objects.get(id=employee_id)
            project.employees.add(employee)
            return Response({'status': 'Employee added'})
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=404)

class MilestoneViewSet(ModelViewSet):
    serializer_class = MilestoneSerializer
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]

    def get_queryset(self):
        return Milestone.objects.filter(project_id=self.kwargs['project_pk'])\
            .select_related('project')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['project'] = Project.objects.get(pk=self.kwargs['project_pk'])
        return context

    @action(detail=True, methods=['post'])
    def mark_complete(self, request, project_pk=None, pk=None):
        milestone = self.get_object()
        milestone.status = 'completed'
        milestone.save()
        return Response({'status': 'Milestone completed'})