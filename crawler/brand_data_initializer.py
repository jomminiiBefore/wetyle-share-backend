# -*- coding: utf-8 -*-

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wetyle_share.settings')

import django
django.setup()

import csv
from product.models import Brand

result = []
with open('./crawler/brand_infos_modified.csv', mode='r') as brand_lists:
    reader = csv.reader(brand_lists, delimiter=',')

    for list in reader:
        result.append(list)

for brand in result:
    print(brand)
    Brand(
        name = brand[0],
        large_image_url = brand[1],
        small_image_url = brand[2],
        description = brand[3],
    ).save()