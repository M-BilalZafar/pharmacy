from django.urls import path , include
from app import views
from .views import *
urlpatterns = [
    path('', HomeView.as_view() , name='Items'),
    path('product-detail/<slug>/', ItemDetailView.as_view() , name='product-detail'),
    path('add-to-cart/<slug>/', add_to_cart , name='add-to-cart'),
    path('order-summary/', OrderSummaryView.as_view() , name='order-summary'),
    path('remove-from-cart/<slug>/', remove_from_cart , name='remove-from-cart'),
    path('remove_single_item_from_cart/<slug>/', remove_single_item_from_cart , name='remove_single_item_from_cart'),
    path('checkout/', views.checkout , name='checkout'),
]