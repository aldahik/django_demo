from django.shortcuts import render, redirect
from .models import Inquiry
from .models import InquiryAnalysis
from .forms import InquiryForm
from django.shortcuts import get_object_or_404
from .services.analysis import process_inquiry_analysis


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
            inquiry = form.save()
            process_inquiry_analysis(inquiry)
            return redirect("get_inquiry", id=inquiry.id)

    return render(
        request,
        "inquiries/inquiry_form.html",
        {"form" : form}
    )

def get_inquiry(request, id: int):
    inquiry = get_object_or_404(Inquiry, id=id)
    analysis = InquiryAnalysis.objects.filter(
        inquiry= inquiry
    ).first()

    return render(
        request,
        "inquiries/inquiry.html",
        {
            "inquiry" : inquiry,
            "analysis": analysis
        }
    )