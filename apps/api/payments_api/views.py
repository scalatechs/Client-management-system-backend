import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Payment, PaymentInvoice
from .serializers import PaymentSerializer, PaymentInvoiceSerializer
from django.shortcuts import get_object_or_404
from apps.projects.models import Project
from apps.customers.models import Customer
from apps.accounts.models import CustomUser
from rest_framework.permissions import AllowAny

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(customer__user=self.request.user)\
            .select_related('project', 'customer')

    def create(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
         # Ensure user is linked to a customer
        if not hasattr(request.user, 'customer'):
            return Response({"error": "User is not associated with a customer"}, status=status.HTTP_400_BAD_REQUEST)
        
        project_id = request.data.get('project')
        if not project_id:
            return Response({"error": "Project id is required"}, status=status.HTTP_400_BAD_REQUEST)

        
        # Retrieve the project instance
        project = get_object_or_404(Project, pk=project_id)

        # Get the customer linked to the user
        customer = request.user.customer

        # Create a serializer context that includes the project.
        serializer_context = self.get_serializer_context()
        serializer_context['project'] = project

        # Instantiate the serializer with the updated context.
        serializer = self.get_serializer(data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        
        
        # Create payment
        payment = Payment.objects.create(
            customer=customer,
            project=project,
            amount=serializer.validated_data['amount'],
            gateway=serializer.validated_data['gateway']
        )
        
        # Create invoice
        invoice = PaymentInvoice.objects.create(
            payment=payment,
            invoice_id=f"INV-{payment.id:08}",
            due_date=project.due_date
        )

        return Response({
            'payment_id': payment.id,
            'invoice_id': invoice.invoice_id,
            'amount': payment.amount
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def process_khalti(self, request, pk=None):
        """Process payment through Khalti gateway"""
        payment = self.get_object()
        
        if payment.status != 'pending':
            return Response({'error': 'Payment already processed'}, status=400)

        # Convert amount to paisa (Khalti requires amount in paisa)
        amount_in_paisa = int(payment.amount * 100)
        
        payload = {
            "return_url": f"{settings.FRONTEND_URL}/api/payments/{payment.id}/verify_khalti/",
            "website_url": settings.FRONTEND_URL,
            "amount": str(amount_in_paisa),
            "purchase_order_id": payment.paymentinvoice.invoice_id,
            "purchase_order_name": f"Payment for {payment.project.title}",
            "customer_info": {
                "name": payment.customer.name,
                "email": payment.customer.email,
                "phone": str(payment.customer.phone)
            }
        }

        headers = {
            'Authorization': f'Key {settings.KHALTI_SECRET_KEY}',
            'Content-Type': 'application/json',
        }

        try:
            response = requests.post(
                "https://dev.khalti.com/api/v2/epayment/initiate/",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            response_data = response.json()
            
            payment.transaction_id = response_data.get('pidx')
            payment.save()
            
            return Response({
                'payment_url': response_data['payment_url'],
                'pidx': response_data['pidx']
            })

        except requests.exceptions.RequestException as e:
            payment.status = 'failed'
            payment.save()
            return Response({'error': str(e)}, status=400)
        
    @action(detail=True, methods=['get'], url_path='verify_khalti', permission_classes=[AllowAny])
    def verify_khalti(self, request, pk=None):
        """Verify payment when user is redirected from Khalti"""
        pidx = request.query_params.get("pidx")  # Get pidx from Khalti redirect URL
        
        if not pidx:
            return Response({'error': 'Missing pidx in query parameters'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Find the payment with this pidx
            payment = Payment.objects.get(transaction_id=pidx)
        except Payment.DoesNotExist:
            return Response({'error': 'Invalid transaction'}, status=status.HTTP_400_BAD_REQUEST)

        # Verify the transaction with Khalti
        verify_url = "https://dev.khalti.com/api/v2/epayment/lookup/"
        headers = {'Authorization': f'Key {settings.KHALTI_SECRET_KEY}'}
        payload = {'pidx': pidx}

        try:
            verify_response = requests.post(verify_url, headers=headers, json=payload)
            verify_response.raise_for_status()
            verify_data = verify_response.json()

            if verify_data['status'] == 'Completed':
                # Update payment status
                payment.status = 'completed'
                payment.save()

                # Deduct the amount from the project
                payment.project.remaining_amount -= payment.amount
                payment.project.save()

                return Response({'status': 'Payment completed'}, status=status.HTTP_200_OK)

            return Response({'status': 'Payment failed'}, status=status.HTTP_400_BAD_REQUEST)

        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
    # @action(detail=True, methods=['post'])
    # def verify_khalti(self, request, pk=None):
    #     """Step 2: Verify Khalti Payment"""
    #     payment = self.get_object()
    #     pidx = payment.transaction_id  # Get stored pidx

    #     if not pidx:
    #         return Response({'error': 'No transaction ID found'}, status=400)

    #     verify_url = "https://dev.khalti.com/api/v2/epayment/lookup/"
    #     headers = {'Authorization': f'Key {settings.KHALTI_SECRET_KEY}'}
    #     payload = {'pidx': pidx}

    #     try:
    #         verify_response = requests.post(verify_url, json=payload, headers=headers)
    #         verify_response.raise_for_status()
    #         verify_data = verify_response.json()

    #         if verify_data['status'] == 'Completed':
    #             payment.status = 'completed'
    #             payment.save()
    #             payment.project.remaining_amount -= payment.amount
    #             payment.project.save()
    #             return Response({'status': 'Payment completed'}, status=status.HTTP_200_OK)

    #         payment.status = 'failed'
    #         payment.save()
    #         return Response({'status': 'Payment failed'}, status=status.HTTP_400_BAD_REQUEST)

    #     except requests.exceptions.RequestException as e:
    #         return Response({'error': str(e)}, status=400)
   


# class KhaltiWebhookView(APIView):
#     def post(self, request):
#         pidx = request.data.get('pidx')
#         try:
#             payment = Payment.objects.get(transaction_id=pidx)
            
#             # Verify transaction with Khalti
#             verify_url = f"https://dev.khalti.com/api/v2/epayment/lookup/{pidx}/"
#             headers = {'Authorization': f'Key {settings.KHALTI_SECRET_KEY}'}
            
#             verify_response = requests.get(verify_url, headers=headers)
#             verify_response.raise_for_status()
#             verify_data = verify_response.json()
            
#             if verify_data['status'] == 'Completed':
#                 payment.status = 'completed'
#                 payment.save()
#                 payment.project.remaining_amount -= payment.amount
#                 payment.project.save()
#                 return Response({'status': 'Payment completed'}, status=status.HTTP_200_OK)
            
#             payment.status = 'failed'
#             payment.save()
#             return Response({'status': 'Payment failed'}, status=status.HTTP_400_BAD_REQUEST)

#         except Payment.DoesNotExist:
#             return Response({'error': 'Invalid transaction'}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

