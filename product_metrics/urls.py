from django.urls import path
from .views import ProductMetricsListView

urlpatterns = [
    path('api/product-metrics/', ProductMetricsListView.as_view(), name='product-metrics-list'),
]

