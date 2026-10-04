from django.shortcuts import render, redirect
from .models import Inquiry
from .forms import InquiryForm
from django.shortcuts import get_object_or_404

def inquiry_list(request):
    inquiries = Inquiry.objects.all()

    return render(
        request,
        "inquiries/inquiry_list.html",
        {"inquiries" : inquiries}
    )

def create_inquiry(request):
    if request.method == "GET":
        form = InquiryForm()
    
    elif request.method == "POST":
        form = InquiryForm(request.POST)

        if form.is_valid():
          form.save()
        return redirect("inquiry_list")

    return render(
        request,
        "inquiries/inquiry_form.html",
        {"form" : form}
    )

def get_inquiry(request, id):
    inquiry = get_object_or_404(Inquiry, id=id)
    return render(
        request,
        "inquiries/inquiry.html",
        {"inquiry" : inquiry}
    )