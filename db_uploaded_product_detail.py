# -*- coding: utf-8 -*-

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wetyle_share.settings')

import django
django.setup()

import csv
from product.models import Product

result = []
with open('product_details.csv', mode='r') as product_details:
    reader = csv.reader(product_details)

    for productdetail in reader:
        result.append(productdetail)

for product in result:
    print(product)
    Product(
        name                 = product[0],
        image_url            = product[1],
        price                = product[2],
        discounted_price     = product[3],
        detailed_info        = product[4],
        add_info             = product[5],
      #  brand_large_image_url      = product[6],
      #  brand_name           = product[8],
        brand_id             = product[9],
      #  category_id          = product[10],
        first_category_id    = product[11],
        second_category_id   = product[12],
        third_category_id    = product[13],        
    ).save()
