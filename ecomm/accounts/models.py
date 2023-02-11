from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save #interesting to explore
from django.dispatch import receiver
from base.emails import send_email_verification_link
from products.models import Product,SizeVariant,ColorVariant
import uuid

# Create your models here.


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100,null=True,blank=True)
    profile_image = models.ImageField(upload_to='profile')


    def get_cart_count(self):
        return CartItems.objects.filter(cart__is_paid = False , cart__user = self.user).count()

class Cart(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='carts')
    is_paid = models.BooleanField(default = False)

    def get_cart_total(self):
        price = []
        for item in self.cart_items.all():
            price.append(item.product.price)
            if item.colorVariant:
                color_variant_price = item.colorVariant.price
                price.append(color_variant_price)
            if item.sizeVariant:
                Size_variant_price = item.sizeVariant.price
                price.append(Size_variant_price)
        return sum(price)

class CartItems(BaseModel):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='cart_items',null = True,blank= True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null= True)
    colorVariant = models.ForeignKey(ColorVariant,on_delete=models.SET_NULL,blank=True,null= True)
    sizeVariant = models.ForeignKey(SizeVariant,on_delete=models.SET_NULL,blank=True,null= True)

    def get_product_price(self):
        price = [self.product.price]

        if self.colorVariant:
            color_variant_price = self.colorVariant.price
            price.append(color_variant_price)
        if self.sizeVariant:
            Size_variant_price = self.sizeVariant.price
            price.append(Size_variant_price)
        return sum(price)



@receiver(post_save,sender = User)
def send_email_token(sender , instance, created, **kwargs):

    try:
        if created:
            email_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = instance ,email_token = email_token)
            profile_obj.save()
            email = instance.email
            send_email_verification_link(email,email_token)
    except Exception as e:
        print(e)

