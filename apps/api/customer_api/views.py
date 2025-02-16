from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.customers.models import Customer, Interaction, CustomerProject
from .serializers import CustomerSerializer, InteractionSerializer, CustomerProjectSerializer
from .permissions import IsAdminOrReadOnly

class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        return Customer.objects.prefetch_related(
            'interactions', 
            'customer_projects__project'
        ).order_by('-last_interaction')

    @action(detail=True, methods=['post'])
    def upload_image(self, request, pk=None):
        customer = self.get_object()
        customer.image = request.FILES.get('image')
        customer.save()
        return Response({'status': 'Image uploaded'})

class InteractionViewSet(ModelViewSet):
    serializer_class = InteractionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Interaction.objects.filter(
            customer_id=self.kwargs['customer_pk']
        ).select_related('customer')

    def perform_create(self, serializer):
        customer = Customer.objects.get(pk=self.kwargs['customer_pk'])
        serializer.save(customer=customer)

class CustomerProjectViewSet(ModelViewSet):
    serializer_class = CustomerProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomerProject.objects.filter(
            customer_id=self.kwargs['customer_pk']
        ).select_related('customer', 'project')