from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet
router = DefaultRouter()
router.register(r'', PaymentViewSet, basename='payment')

urlpatterns = [
    # path('webhook/<str:gateway>/', PaymentWebhookView.as_view(), name='payment-webhook'),
    # path('khalti-webhook/', KhaltiWebhookView.as_view(), name='khalti-webhook'),
    # path('payments/webhook/', KhaltiWebhookView.as_view(), name='khalti-webhook'),
    path('', include(router.urls)),
]