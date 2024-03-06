from django.urls import include, path
from rest_framework.routers import DefaultRouter

from snippets.views import PhoneListAPIView, BillingObjectAPIView, BillingAPIView

app_name = "snippets"

urlpatterns = [
    # path('drf-auth/', include('rest_framework.urls')),
    path('v1/testlist/', PhoneListAPIView.as_view()),
    path('v1/testbill/<slug:billing_phone_number>', BillingObjectAPIView.as_view()),
    path('v1/testbill/', BillingAPIView.as_view()),
]
