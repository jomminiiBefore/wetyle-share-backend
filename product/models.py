from django.db import models
from user.models import User

class Product(models.Model):
    name            = models.TextField()    
    first_category  = models.ForeignKey('FirstCategory', on_delete = models.SET_NULL, null = True)
    second_category = models.ForeignKey('SecondCategory', on_delete = models.SET_NULL, null = True)
    third_category  = models.ForeignKey('ThirdCategory', on_delete = models.SET_NULL, null = True)
    brand           = models.ForeignKey('Brand', on_delete = models.SET_NULL, related_name = 'brands', null = True)
    price           = models.IntegerField(default = 0)
    discounted_price= models.IntegerField(default = 0)
    point           = models.IntegerField(default = 0)
    detailed_info   = models.TextField()
    add_info        = models.TextField()
    created_at      = models.DateTimeField(auto_now_add = True)
    updated_at      = models.DateTimeField(auto_now = True)
    product_color   = models.ManyToManyField('Color', through = 'ProductColor')
    product_size    = models.ManyToManyField('Size', through = 'ProductSize')
    product_like    = models.ManyToManyField(User, through = 'ProductLike')

    class Meta:
        db_table = 'products'

class FirstCategory(models.Model):
    name            = models.CharField(max_length = 50)

    class Meta:
        db_table = 'first_categories'

class SecondCategory(models.Model):
    name            = models.CharField(max_length = 50)
    first_category  = models.ForeignKey('FirstCategory', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'second_categories'

class ThirdCategory(models.Model):
    name            = models.CharField(max_length = 50)
    first_category   = models.ForeignKey('FirstCategory', on_delete = models.SET_NULL, null = True)
    second_category = models.ForeignKey('SecondCategory', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'third_categories'

class Brand(models.Model):
    name            = models.CharField(max_length = 50)
    description     = models.CharField(max_length = 500)
    created_at      = models.DateTimeField(auto_now_add = True)
    updated_at      = models.DateTimeField(auto_now = True)    
    small_image_url = models.URLField(max_length = 2000)
    large_image_url = models.URLField(max_length = 2000)

    class Meta:
        db_table = 'brands'

class ProductDetailImage(models.Model):
    image_url       = models.URLField(max_length = 2000)
    product         = models.ForeignKey('Product', on_delete = models.CASCADE)

    class Meta:
        db_table = 'product_detail_images'

class ProductLike(models.Model):
    product         = models.ForeignKey('Product', on_delete = models.CASCADE)
    user            = models.ForeignKey(User, on_delete = models.CASCADE)
    created_at      = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        db_table = 'product_likes'

class ProductInqury(models.Model):
    decription      = models.CharField(max_length = 500)
    user            = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    is_answer       = models.BooleanField(default = False)
    description     = models.CharField(max_length = 500)
    product         = models.ForeignKey('Product', on_delete = models.CASCADE, null = True)
    
    class Meta:
        db_table = 'product_inqueries'

class ProductColor(models.Model):
    product         = models.ForeignKey('Product', on_delete = models.SET_NULL, null = True)
    color           = models.ForeignKey('Color', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'product_colors'

class Color(models.Model):
    name            = models.CharField(max_length = 50)

    class Meta:
        db_table = 'colors'

class ProductSize(models.Model):
    product         = models.ForeignKey('Product', on_delete = models.SET_NULL, null = True)
    size            = models.ForeignKey('Size', on_delete = models.SET_NULL, null = True)
   
    class Meta:
        db_table = 'product_sizes'

class Size(models.Model):
    name            = models.CharField(max_length = 50)

    class Meta:
        db_table = 'sizes'

class ProductStock(models.Model):
    product         = models.ForeignKey('Product', on_delete = models.SET_NULL, null = True)
    color           = models.ForeignKey('Color', on_delete = models.SET_NULL, null = True)
    size            = models.ForeignKey('Size', on_delete = models.SET_NULL, null = True)
    stock           = models.IntegerField()

    class Meta:
        db_table = 'product_stocks'

class OrderedProduct(models.Model):
    order           = models.ForeignKey('Order', on_delete = models.SET_NULL, null = True)
    product         = models.ForeignKey('Product', on_delete = models.SET_NULL, null = True)
    size            = models.ForeignKey('Size', on_delete = models.SET_NULL, null = True)
    color           = models.ForeignKey('Color', on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = 'ordered_products'

class Order(models.Model):
    user            = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    shipping        = models.ForeignKey('Shipping', on_delete = models.SET_NULL, null = True)
    created_at      = models.DateTimeField(auto_now_add = True)
    updated_at      = models.DateTimeField(auto_now = True)
    shipping_address= models.CharField(max_length = 500)

    class Meta:
        db_table = 'orders'

class Shipping(models.Model):
    shipping        = models.CharField(max_length = 50)

    class Meta:
        db_table = 'shippings'
