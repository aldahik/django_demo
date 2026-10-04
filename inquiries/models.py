from django.db import models

class Inquiry(models.Model):
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    description = models.TextField()
    status = models.CharField(max_length=50, default="new")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.status}"
    
class InquiryAnalysis(models.Model):
    inquiry = models.OneToOneField(
        Inquiry,
        on_delete=models.CASCADE,
        related_name="analysis"
        )
    
    material = models.CharField(max_length=100, null=True)
    quantity = models.PositiveIntegerField(null=True)
    thickness_mm = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    width_mm = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    height_mm = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    deadline = models.DateField(null=True)