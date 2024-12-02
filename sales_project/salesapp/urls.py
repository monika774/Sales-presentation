from django.urls import path, include
from .views import SaleDataAPIView, DescriptiveAnalysis, PredictiveAnalysis
from . import views

urlpatterns = [
    path('sales/', SaleDataAPIView.as_view(), name='sales-api'),
    path('sales/<int:pk>/', SaleDataAPIView.as_view(), name='sales-api-detail'),
    path('analysis/descriptive/', DescriptiveAnalysis.as_view(), name='descriptive-analysis'),
    path('analysis/predictive/', PredictiveAnalysis.as_view(), name='predictive-analysis'),
    # path('dashboard/', DjangoDash.as_view(), name='sales-dashboard'), 
    # path('dashboard/', dash_app.as_view(), name='dashboard'),   
    # path('django_plotly_dash/', include('django_plotly_dash.urls')),  # Dash routes
    path('', views.dash_view, name='dash_view'),
  
]
