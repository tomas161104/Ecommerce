from django.db import models
from django.conf import settings

PAYMENT_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
)

PAYMENT_METHOD_CHOICES = (
    ('card', 'Card'),
    ('paypal', 'PayPal'),
    ('stripe', 'Stripe'),
    ('cash', 'Cash'),
)

class Payment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='payments',
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.id} - {self.user.username} - {self.amount} USD"
