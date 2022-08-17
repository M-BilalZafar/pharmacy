import imp
from importlib.resources import contents
from multiprocessing import context
from django.contrib import messages
from django.shortcuts import render , get_object_or_404 , redirect
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView , DetailView , View
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
app_name='app'


class HomeView(ListView):
    model = Item
    paginate_by= 8
    template_name = "home-page.html"


class ItemDetailView(DetailView):
    model = Item
    template_name = "product-page.html"


login_required
def checkout(request):
    return render(request,"checkout-page.html")

login_required
def add_to_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_item ,created= OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
        )
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(item__slug=slug ).exists():
            
            order_item.quantity +=1
            order_item.save()
            messages.info(request,"This Item quantity was Updated.")
            return redirect('app:order-summary')
        else:
            messages.info(request,"This Item was added to your Cart.")
            order.items.add(order_item)
            return redirect('app:product-detail',slug=slug)
    else:
        ordered_date=timezone.now()
        order=Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,"This Item was added to your Cart.")
        return redirect('app:product-detail',slug=slug)
    return redirect('app:product-detail',slug=slug)   
            
        
        
def remove_from_cart(request , slug):
    item =get_object_or_404(Item,slug=slug)
    order_qs=Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False,
            )[0]
            order.items.remove(order_item)
            messages.info(request,"This Item was removed from your Cart.")
            return redirect('app:order-summary')
        else:
            messages.info(request,"This Item was not in your Cart.")
            return redirect('app:product-detail',slug=slug)    
            
            
    else:
        messages.info(request,"You do not have an active order.")
        return redirect('app:product-detail',slug=slug)
    
    
    return redirect('app:product-detail',slug=slug)


def remove_single_item_from_cart(request , slug):
    item =get_object_or_404(Item,slug=slug)
    order_qs=Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False,
            )[0]
            if order_item.quantity > 1:
                
                order_item.quantity -=1
                order_item.save()
            
            else:
                order.items.remove(order_item)
            messages.info(request,"This Item quantity was updated.")

        else:
            messages.info(request,"This Item was not in your Cart.")
            return redirect('app:order-summary')    
            
            
    else:
        messages.info(request,"You do not have an active order.")
        return redirect('app:order-summary')
    
    
    return redirect('app:order-summary')
           
            
            
class OrderSummaryView(LoginRequiredMixin ,View):
    def get(self ,*args, **kwargs):
        
        try:
            order=Order.objects.get(user=self.request.user ,ordered=False)
            context={
                'object':order
            }
            return render(self.request,"order_summary.html",context)
        except ObjectDoesNotExist:
            messages.error(self.request,"You Don't have an active order"  )
            return redirect('/')    
    
