from django.db import models

# Create your models here.
class Review(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    img = models.ImageField(upload_to='product/reviews')
    content = models.CharField(max_length=255)