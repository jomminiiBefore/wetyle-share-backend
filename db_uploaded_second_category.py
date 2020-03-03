# -*- coding: utf-8 -*-

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wetyle_share.settings')

import django
django.setup()

import csv
from product.models import SecondCategory, FirstCategory

result = []
with open('second_category.csv', mode='r') as second_category:
    reader = csv.reader(second_category)

    for secondcategory in reader:
        result.append(secondcategory)

for second in result:
    print(second)
    SecondCategory(
        name              = second[0],
        first_category_id = second[1]
    ).save()
