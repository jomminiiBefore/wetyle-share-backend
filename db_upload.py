# -*- coding: utf-8 -*-

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wetyle_share.settings')

import django
django.setup()

import csv
from user.models    import *
from card.models    import *
from product.models import *

# User
print("user")
def add_user():
    with open('./upload/user.csv', mode='r') as user_lists:
        reader = csv.reader(user_lists, delimiter=',')
 
        for user in list(reader)[1:]:
            print(user)
            User(
                login_id    = user[0],
                password    = user[1],
                nickname    = user[2],
                gender      = user[3],
                email       = user[4],
                description = user[5],
                image_url   = user[6],
            ).save()
add_user()

print("collection")
# Collection
def add_collection():
    with open('./upload/collection.csv', mode='r') as collection_lists:
        reader = csv.reader(collection_lists, delimiter=',')
         
        for collection in list(reader)[1:]:
            Collection(
                name        = collection[0],
                description = collection[1],
                user_id     = collection[2],
                image_url   = collection[3],
            ).save()
add_collection()

print("style")
# Style
def add_style():
    with open('./upload/style.csv', mode='r') as style_lists:
        reader = csv.reader(style_lists, delimiter=',')
    
        for style in list(reader)[1:]:
            print(style)
            make = Style.objects.create(
                description = style[0],
                user_id = style[2],
            )
            StyleImage.objects.create(
                image_url = style[1],
                style_id  = make.id
            )
add_style()

print("collection_style")
# Collection_style
def add_collection_style():
    with open('./upload/collection_style.csv', mode='r') as collection_style_lists:
        reader = csv.reader(collection_style_lists, delimiter=',')
    
        for collection_style in list(reader)[1:]:
            make = CollectionStyle.objects.create(
                style_id      = collection_style[0],
                collection_id = collection_style[1],
            )
add_collection_style()

print("stylecomment")
# StyleComment
def add_style_comment():
    with open('./upload/style_comment.csv', mode='r') as style_comment_lists:
        reader = csv.reader(style_comment_lists, delimiter=',')
    
        for comment in list(reader)[1:]:
            StyleComment(
                description = comment[0],
                style_id = comment[1],
                user_id = comment[2],
            ).save()
add_style_comment()

print("stylerelateditem")
# StyleRelatedItem
def add_style_related_item():
    with open('./upload/style_related_item.csv', mode='r') as style_related_item_lists:
        reader = csv.reader(style_related_item_lists, delimiter=',')
    
        for item in list(reader)[1:]:
            StyleRelatedItem(
                pants     = item[0],
                skirt     = item[1],
                shoes     = item[2],
                bag       = item[3],
                accessory = item[4],
                etc       = item[5],
                style_id  = item[6],
            ).save()
add_style_related_item()

print("stylelike")
# StyleLike
def add_style_like():
    with open('./upload/style_like.csv', mode='r') as style_like_lists:
        reader = csv.reader(style_like_lists, delimiter=',')
    
        for item in list(reader)[1:]:
            StyleLike(
                style_id  = item[0],
                user_id   = item[1],
            ).save()
add_style_like()

print("brand")
# brand
def add_brand():
    with open('./upload/styleshare_brand - 브랜드 정보.csv', mode='r') as brand_lists:
        result = []
        reader = csv.reader(brand_lists, delimiter=',')

        for brand_list in list(reader)[1:]:
            result.append(brand_list)

    for brand in result:
        print(brand)
        Brand(
            name = brand[0],
            large_image_url = brand[1],
            small_image_url = brand[2],
            description = brand[3],
        ).save()
add_brand()

print("firstcategory")
# first category
def add_first_category():
    with open('./upload/first_category.csv', mode='r') as first_category:
        result = []
        reader = csv.reader(first_category)

        for firstcategory in reader:
            result.append(firstcategory)

    for first in result:
        print(first)
        FirstCategory(
            name = first[0]
        ).save()
add_first_category()

print("secondcategory")
# second category
def add_second_category():
    with open('./upload/second_category.csv', mode='r') as second_category:
        result = []
        reader = csv.reader(second_category)

        for secondcategory in reader:
            result.append(secondcategory)

    for second in result:
        print(second)
        SecondCategory(
            name              = second[0],
            first_category_id = second[1]
        ).save()
add_second_category()

print("thirdcategory")
# third category
def add_third_category():
    with open('./upload/third_category.csv', mode='r') as third_category:
        result = []
        reader = csv.reader(third_category)

        for thirdcategory in reader:
            result.append(thirdcategory)

    for third in result:
        print(third)
        ThirdCategory(
            name               = third[0],
            first_category_id  = third[1],
            second_category_id = third[2]
        ).save()
add_third_category()

print("product")
#Product
def add_product():
    with open('./upload/products.csv', mode='r') as product_lists:
        reader = csv.reader(product_lists, delimiter=',')

        for product in list(reader)[1:]:
            make = Product.objects.create(
                name               = product[0],
                image_url          = product[1],
                first_category_id  = product[6] ,
                second_category_id = product[7],
                third_category_id  = product[8],
                brand_id           = product[5],
                price              = product[2],
                discounted_price   = product[3],
                point              = int(product[3]) * 0.01,
                add_info           = str(product[4])
            )
            for i in range(55)[9:]:
                if product[i] :
                    ProductDetailImage.objects.create(
                        image_url          = product[i],
                        product_id         = make.id,
                    )
add_product() 

print("product color")
# Product color
def add_product_color():
    with open('./upload/color.csv', mode='r') as color_lists:
       reader = csv.reader(color_lists, delimiter=',')

       for color in list(reader):
           Color.objects.create(
               name = color[0],
            )
add_product_color()

print("product size")
# Product size
def add_product_size():
    with open('./upload/size.csv', mode='r') as size_lists:
        reader = csv.reader(size_lists, delimiter=',')

        for size in list(reader):
            Size.objects.create(
                name = size[0],
            )
add_product_size()

print("product colors")
# product_colors
def product_colors():
    with open('./upload/color.csv', mode='r') as color_lists:
        reader = csv.reader(color_lists, delimiter=',')

        for i in range(len(Product.objects.all())+1)[1:]:
            for j in range(len(Color.objects.all())+1)[1:]:
                ProductColor.objects.create(product_id = i, color_id = j)
product_colors()

print("product sizes")
# product_sizes
def product_sizes():
    with open('./upload/size.csv', mode='r') as size_lists:
        reader = csv.reader(size_lists, delimiter=',')

        for i in range(len(Product.objects.all())+1)[1:]:
            for j in range(len(Size.objects.all())+1)[1:]:
               ProductSize.objects.create(product_id = i, size_id = j)
product_sizes()
