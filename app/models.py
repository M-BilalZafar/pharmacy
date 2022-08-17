from pydoc import describe
from sre_parse import CATEGORIES
from tracemalloc import get_object_traceback
from django.db import models
from django.conf import settings
from django.shortcuts import reverse
# Create your models here.

Category_Choice =(
    ('Tablets','Tablets'),
    ('Capsules','Capsule'),
    ('Injections','Injections'),
    
)
Label_Choice =(
    ('P','primary'),
    ('S','secondary'),
    ('D','danger'),
    
)

class Item(models.Model):
    title = models.CharField( max_length=50)
    price =models.FloatField()
    discount_price =models.FloatField(blank=True,null=True)
    category = models.CharField(choices=Category_Choice, max_length=15)
    label = models.CharField(choices=Label_Choice, max_length=15)
    slug = models.SlugField()
    description= models.TextField()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("app:product-detail", kwargs={"slug": self.slug})
    
    
    
    def get_add_to_cart(self):
        return reverse("app:add-to-cart", kwargs={"slug": self.slug})
    
   
   
    def get_remove_from_cart(self):
        return reverse("app:remove-from-cart", kwargs={"slug": self.slug})
    




class OrderItem(models.Model):
    user= models.ForeignKey( settings.AUTH_USER_MODEL,on_delete=models.CASCADE )
    item=models.ForeignKey(Item, on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)  
    quantity=models.IntegerField(default=1)



    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
    
    def get_total_price(self):
        return self.quantity * self.item.price
    
    
    
    def get_discount_price(self):
        return self.quantity * self.item.discount_price
    
    
    def get_saved_price(self):
        return self.get_total_price() - self.get_discount_price()
    
    
    def get_final_price(self):
        if self.get_discount_price():
            return self.get_discount_price()
        
        return self.get_total_price()


class Order(models.Model):
    user= models.ForeignKey( settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items=models.ManyToManyField(OrderItem)
    ordered=models.BooleanField(default=False)  
    start_date = models.DateTimeField( auto_now_add=True) 
    ordered_date = models.DateTimeField() 
    
    
    def __str__(self):
        return self.user.username
    
    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total    
        
    
    
    
        
    

    
     
     
    
