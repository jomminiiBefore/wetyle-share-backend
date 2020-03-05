from user.models import User
from product.models import Product

from django.db import models

class Collection(models.Model):
    name        = models.CharField(max_length = 50)
    image_url   = models.URLField(max_length = 2000)
    description = models.CharField(max_length = 500)
    user        = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'collections')
    created_at  = models.DateTimeField(auto_now_add = True)
    updated_at  = models.DateTimeField(auto_now = True)
    collection_follower = models.ManyToManyField(User, through = 'CollectionFollower')
    collection_style    = models.ManyToManyField('Style', through = 'CollectionStyle')
    # 리뷰 class 등록 후 컬렉션 리뷰 다대다 작성
    # Q&A class 등록 후 컬렉션 Q&A 다대다 작성

    class Meta:
        db_table = 'collections'

class Style(models.Model):
    description = models.CharField(max_length = 500)
    user        = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'styles')
    style_like  = models.ManyToManyField(User, through = 'StyleLike')
    style_related_selling_item = models.ManyToManyField(Product, through = 'StyleRelatedSellingItem')
    created_at  = models.DateTimeField(auto_now_add = True)
    updated_at  = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'styles'

class StyleImage(models.Model):
    image_url   = models.URLField(max_length = 2000)
    style       = models.ForeignKey(Style, on_delete = models.CASCADE)
    
    class Meta:
        db_table = 'style_images'

class StyleComment(models.Model):
    description = models.CharField(max_length = 200)
    style       = models.ForeignKey(Style, on_delete = models.CASCADE, related_name = 'comments')
    user        = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'comments')
    created_at  = models.DateTimeField(auto_now_add = True)
    updated_at  = models.DateTimeField(auto_now = True)

    class Meta:
        db_table  = 'style_comments'

class StyleLike(models.Model):
    user       = models.ForeignKey(User, on_delete = models.CASCADE)
    style      = models.ForeignKey(Style, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'style_likes'

class CollectionStyle(models.Model):
    collection = models.ForeignKey(Collection, on_delete = models.CASCADE)
    style      = models.ForeignKey(Style, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'collection_styles'

class StyleRelatedItem(models.Model):
    pants      = models.CharField(max_length = 50)
    skirt      = models.CharField(max_length = 50)
    shoes      = models.CharField(max_length = 50)
    bag        = models.CharField(max_length = 50)
    accessory  = models.CharField(max_length = 50)
    etc        = models.CharField(max_length = 50)
    style      = models.ForeignKey(Style, on_delete = models.CASCADE, related_name = 'style_related_items')

    class Meta:
        db_table = 'style_related_items'

class StyleRelatedSellingItem(models.Model):
    style      = models.ForeignKey(Style, on_delete = models.CASCADE)
    product    = models.ForeignKey(Product, on_delete = models.CASCADE)

    class Meta:
        db_table = 'style_related_selling_items'

class CollectionFollower(models.Model):
    user       = models.ForeignKey(User, on_delete = models.CASCADE)
    collection = models.ForeignKey('Collection', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'collection_followers'
