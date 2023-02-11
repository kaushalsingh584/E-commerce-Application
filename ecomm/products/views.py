from django.shortcuts import render,redirect
from .models import Product
from django.http import HttpResponseNotFound,HttpResponseRedirect

# Create your views here.

def get_products(request,slug):
    try:
        product = Product.objects.get(slug = slug)
        context = {'product' : product} 
        size = request.GET.get('size')
        if size is not None:
            price = product.get_product_by_size(size)
            print(price)
            context['selected_size'] = size
            context['updated_price'] = price 

        return render(request,'products/products.html',context)
    except Exception as e:
        print(e)
        return HttpResponseNotFound("Page not found")








