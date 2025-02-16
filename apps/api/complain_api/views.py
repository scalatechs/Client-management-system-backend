from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Complaint
from .serializers import ComplaintSerializer, CreateComplaintSerializer
from .permissions import IsComplainantOrAdmin

class ComplaintViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsComplainantOrAdmin]
    
    def get_queryset(self):
        return Complaint.objects.select_related('project', 'user')\
            .filter(user=self.request.user)\
            .order_by('-date_filed')

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateComplaintSerializer
        return ComplaintSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        complaint = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(Complaint.STATUS_CHOICES).keys():
            return Response({'error': 'Invalid status'}, status=400)
            
        complaint.status = new_status
        complaint.save()
        return Response({'status': 'Status updated successfully'})