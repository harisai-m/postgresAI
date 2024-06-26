# ml_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('ml-features/', views.ml_features, name='ml_features'),
    path('data_analysis/', views.data_analysis, name='data_analysis'), 
    path('timeseries_analysis/', views.timeseries_analysis, name='timeseries_analysis'), 
    path('sales_analysis/', views.sales_analysis, name='sales_analysis'),
    path('model_list/', views.model_list, name='model_list'),
    path('model_details/<str:model_name>/', views.model_details, name='model_details'),
    path('data_analysis/<str:model_name>/', views.data_analysis_model, name='data_analysis_model'),
    path('forecasting/', views.forecasting, name='forecasting'),
    path('Sales_Pridiction/<str:model_name>/', views.Sales_Pridiction, name='Sales_Pridiction'),
    path('Capacity_Planing/<str:model_name>/', views.Capacity_Planing, name='Capacity_Planing'),
    path('Future_Trends/<str:model_name>/', views.Future_Trends, name='Future_Trends'),
    path('Stockmarket_prediction/<str:model_name>/', views.Stockmarket_Prediction, name='Stockmarket_Prediction'),
    path('shampoo_sales_prediction/', views.shampoo_sales_prediction, name='shampoo_sales_prediction'),
    path('disk_usage_prediction/', views.disk_usage_prediction, name='disk_usage_prediction'),
   
]
