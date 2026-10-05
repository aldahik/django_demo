from decimal import Decimal
import logging

from .ai import analyze_inquiry
from inquiries.models import InquiryAnalysis
from inquiries.models import Inquiry


def process_inquiry_analysis(inquiry: Inquiry) -> None:
    logger = logging.getLogger(__name__)
    try:  
        result = analyze_inquiry(inquiry.description)

        InquiryAnalysis.objects.create(
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
        logger.exception("AI analysis failed for inquiry %s", inquiry.id)
