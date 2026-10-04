from django.db import models

class Inquiry(models.Model):
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    description = models.TextField()
    quantity = models.PositiveIntegerField(null=True, blank=True)
    material = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=50, default="new")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.status}"