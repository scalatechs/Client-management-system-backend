from rest_framework import serializers
from .models import Payment, PaymentInvoice

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'project', 'amount', 'gateway', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']

    def validate_amount(self, value):
        project = self.context['project']
        if value > project.remaining_amount:
            raise serializers.ValidationError("Payment amount exceeds remaining project amount")
        return value


class PaymentInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentInvoice
        fields = ['invoice_id', 'due_date', 'is_paid']