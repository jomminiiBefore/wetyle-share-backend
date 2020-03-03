# -*- coding: utf-8 -*-

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wetyle_share.settings')

import django
django.setup()

import csv
from product.models import ProductDetailImage

result = []
with open('product_detail_images.csv', mode='r') as brand_lists:
    reader = csv.reader(brand_lists, delimiter=',')

    for image in reader:
        result.append(image)

for detail_image in result:
    print(detail_image)
    ProductDetailImage(
        product_id = detail_image[0],
        image_url = detail_image[1],
    ).save()
