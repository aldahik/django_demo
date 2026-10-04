from django import forms
from .models import Inquiry

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = [
            "customer_name",
            "email",
            "description",
            "quantity",
            "material",
        ]