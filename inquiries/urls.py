from django.urls import path
from . import views

urlpatterns = [
    path("", views.inquiry_list, name="inquiry_list"),
    path("new/", views.create_inquiry, name="create_inquiry"),
    path("<int:id>", views.get_inquiry, name="get_inquiry")
]
