from rest_framework import viewsets
from apps.payments.models import Payment
from apps.payments.api.serializer import PaymentSerializer
from rest_framework.permissions import IsAuthenticated

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='completed', transaction_id='demo123')
