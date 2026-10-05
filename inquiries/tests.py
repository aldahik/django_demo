from datetime import date
from decimal import Decimal
from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from inquiries.models import Inquiry, InquiryAnalysis

from inquiries.schemas import AnalysisResult
from inquiries.services.analysis import process_inquiry_analysis

class InquiryCreateViewTests(TestCase):

    @patch("inquiries.views.process_inquiry_analysis")
    def test_valid_post_creates_inquiry(self, mock_process_analysis):

        response = self.client.post(
            reverse("create_inquiry"),
            {
                "customer_name": "Test Customer",
                "email": "test@example.com",
                "description": "I need 20 aluminium parts.",
            },
        )

        self.assertEqual(Inquiry.objects.count(), 1)

        inquiry = Inquiry.objects.first()

        self.assertEqual(inquiry.customer_name, "Test Customer")
        self.assertEqual(inquiry.email, "test@example.com")
        self.assertEqual(
            inquiry.description,
            "I need 20 aluminium parts.",
        )

        self.assertRedirects(
            response,
            reverse("get_inquiry", args=[inquiry.id]),
        )

        mock_process_analysis.assert_called_once_with(inquiry)


    @patch("inquiries.views.process_inquiry_analysis")
    def test_invalid_post_does_not_create_inquiry(self, mock_process_analysis):

        response = self.client.post(
            reverse("create_inquiry"),
            {
                "customer_name": "Test Customer",
                "email": "not-an-email",
                "description": "Need parts",
            },
        )

        self.assertEqual(Inquiry.objects.count(), 0)

        self.assertTemplateUsed(
            response,
            "inquiries/inquiry_form.html",
        )

        mock_process_analysis.assert_not_called()
        self.assertEqual(response.status_code, 200)


    def test_existing_inquiry_returns_detail_page(self):

        inquiry = Inquiry.objects.create(
            customer_name="test",
            email="test@example.com",
            description="20 Alumimum rods 1x12x3 by 10/10/2026",
        )

        response = self.client.get(
            reverse("get_inquiry", args= [inquiry.id])
        )

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(
            response,
            "inquiries/inquiry.html",
        )

        self.assertEqual(response.context["inquiry"], inquiry)


    def test_nonexistent_inquiry_returns_404(self):

        response = self.client.get(
            reverse("get_inquiry", args= [999])
        )

        self.assertEqual(response.status_code, 404)


class InquiryAnalysisServiceTests(TestCase):

    @patch("inquiries.services.analysis.analyze_inquiry")
    def test_process_inquiry_analysis_creates_analysis(self, mock_analyze):

        inquiry = Inquiry.objects.create(
            customer_name="test",
            email="test@example.com",
            description="20 Aluminium rods 1x12x3 by 10/10/2026",
        )

        mock_analyze.return_value = AnalysisResult(
            material="Aluminium",
            quantity=20,
            width_mm=1,
            thickness_mm=3,
            height_mm=12,
            deadline=date(2026, 10, 10),
        )

        process_inquiry_analysis(inquiry)
        self.assertEqual(InquiryAnalysis.objects.count(), 1)
        analysis= InquiryAnalysis.objects.get(inquiry=inquiry)

        self.assertEqual(analysis.material, "Aluminium")
        self.assertEqual(analysis.quantity, 20)
        self.assertEqual(analysis.width_mm, Decimal(1))
        self.assertEqual(analysis.thickness_mm, Decimal(3))
        self.assertEqual(analysis.height_mm, Decimal(12))
        self.assertEqual(analysis.deadline, date(2026, 10, 10))
        mock_analyze.assert_called_once_with(inquiry.description)

    @patch("inquiries.services.analysis.analyze_inquiry")
    def test_process_inquiry_analysis_does_not_create_analysis_when_ai_fails(self, mock_analyze):

        inquiry = Inquiry.objects.create(
            customer_name="test",
            email="test@example.com",
            description="20 Aluminium rods 1x12x3 by 10/10/2026",
        )

        mock_analyze.side_effect = Exception("AI service unavailable")

        process_inquiry_analysis(inquiry)
        
        self.assertEqual(InquiryAnalysis.objects.count(), 0)
        self.assertTrue(Inquiry.objects.filter(id=inquiry.id).exists())
        mock_analyze.assert_called_once_with(inquiry.description)