from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,"home-page.html")



def product_detail(request):
    return render(request,"product-page.html")



def checkout(request):
    return render(request,"checkout-page.html")



