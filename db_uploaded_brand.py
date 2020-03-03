# -*- coding: utf-8 -*-

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wetyle_share.settings')

import django
django.setup()

import csv
from product.models import Brand 

result = []
with open('brand_infos_modified.csv', mode='r') as brand:
    reader = csv.reader(brand)

    for list in reader:
        result.append(list)

for element in result:
    print(element)
    Brand(
        name                 = element[0],
        large_image_url      = element[1], 
        small_image_url      = element[2],
        description          = element[3],        
    ).save()
