from rest_framework import serializers
from apps.payments.models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'user', 'amount', 'method', 'status', 'transaction_id', 'created_at']
        read_only_fields = ['id', 'user', 'status', 'transaction_id', 'created_at']
