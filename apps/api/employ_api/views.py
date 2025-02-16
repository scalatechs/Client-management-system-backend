from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.employes.models import Employee, Contract, EmployeeProjectAssignment
from .serializers import EmployeeSerializer, ContractSerializer, EmployeeProjectAssignmentSerializer
from .permissions import IsAdminOrEmployeeOwner

class EmployeeViewSet(ModelViewSet):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmployeeOwner]
    
    def get_queryset(self):
        return Employee.objects.select_related(
            'user', 'contract_details'
        ).prefetch_related(
            'project_assignments__project'
        ).all()

    @action(detail=True, methods=['patch'], url_path='upload-image')
    def upload_image(self, request, pk=None):
        employee = self.get_object()
        employee.image = request.FILES.get('image')
        employee.save()
        return Response({'status': 'Image uploaded'})

class ContractViewSet(ModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEmployeeOwner]

    def get_queryset(self):
        return Contract.objects.filter(
            employee_id=self.kwargs['employee_pk']
        ).select_related('employee')

class EmployeeProjectAssignmentViewSet(ModelViewSet):
    serializer_class = EmployeeProjectAssignmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return EmployeeProjectAssignment.objects.filter(
            employee_id=self.kwargs['employee_pk']
        ).select_related('project')