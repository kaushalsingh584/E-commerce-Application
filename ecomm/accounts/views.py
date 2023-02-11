from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from .models import Cart,CartItems
from products.models import Product,SizeVariant

# Create your views here.


def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = email)
        if not user_obj.exists():
            messages.warning(request, "Account not found")
            return HttpResponseRedirect(request.path_info)
            
        user_obj = authenticate(username = email, password = password)

        if not user_obj:
            messages.warning(request, "Not valid Crendentials")
            return HttpResponseRedirect(request.path_info)


        if not user_obj.profile.is_email_verified: # using the related name profile
            messages.warning(request, "Your email is not verified")
            return HttpResponseRedirect(request.path_info)

        if user_obj:
            login(request,user_obj)
            return redirect('/')

    return render(request,'accounts/login.html')


def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(request.POST)
        user_obj = User.objects.filter(username = email)

        if user_obj.exists():
            messages.warning(request,'Email is already registered')
            return HttpResponseRedirect(request.path_info)  # it automatically gets the path and returns to the same page
        user_obj = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            email = email,
            username = email)
        user_obj.set_password(password)
        user_obj.save()
        messages.warning(request,"An email has been sent to your mail")
        return HttpResponseRedirect(request.path_info)

        print(first_name)
    return render(request, 'accounts/register.html')



#  created the corresponding profile model and verifies the email_verified
def activate_email(request,email_token):

    try:
        user = Profile.objects.get(email_token = email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    except Exception as e:
        print(e)
        return HttpResponse("Invalid Token")


def add_to_cart(request,uid):
    variant = request.GET.get('variant')
    product = Product.objects.get(uid = uid)
    user = request.user
    cart,_ = Cart.objects.get_or_create(user = user,is_paid = False) # if there is cart then ok otherwise create one
    
    cart_item = CartItems.objects.create(
        cart = cart,
        product = product,
    )
    if variant:
        size_variant = SizeVariant.objects.get(size_name = variant)
        cart_item.sizeVariant = size_variant
        cart_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_cart(request,cart_item_uid):
    print("hello")
    try:
        print(str(cart_item_uid))
        product  = Product.objects.get(uid = cart_item_uid)
        cart_item = CartItems.objects.filter(product = product).first()
        cart_item.delete()
        print("deleted")
    except Exception as e:
        print("exception" ,e)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def cart(request):
    context = {'cart' : Cart.objects.get(is_paid = False, user = request.user)}
    return render(request,'accounts/cart.html',context)

