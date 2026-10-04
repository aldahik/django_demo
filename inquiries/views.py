from django.shortcuts import render, redirect
from .models import Inquiry
from .models import InquiryAnalysis
from .forms import InquiryForm
from django.shortcuts import get_object_or_404
from .services.ai import analyze_inquiry
from decimal import Decimal


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

            try:  
                result = analyze_inquiry(inquiry.description)

                analysis = InquiryAnalysis.objects.create(
                    inquiry= inquiry,
                    material= result.material,
                    quantity= result.quantity,
                    thickness_mm = (Decimal(str(result.thickness_mm))
                                    if result.thickness_mm is not None else None),

                    width_mm= (Decimal(str(result.width_mm))
                            if result.width_mm is not None else None),
                            
                    height_mm= ((Decimal(str(result.height_mm)) 
                                if result.height_mm is not None else None)),

                    deadline= result.deadline,
                )

            except Exception as e:
                print(f"AI analysis failed: {e}")

            return redirect("get_inquiry", id=inquiry.id)

    return render(
        request,
        "inquiries/inquiry_form.html",
        {"form" : form}
    )

def get_inquiry(request, id):
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