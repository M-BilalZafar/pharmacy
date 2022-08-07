from django.urls import path , include
from app import views
urlpatterns = [
    path('', views.index , name='index'),
    path('product-detail/', views.product_detail , name='product_detail'),
    path('checkout/', views.checkout , name='checkout'),
]