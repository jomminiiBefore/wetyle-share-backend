# -*- coding: utf-8 -*-

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wetyle_share.settings')

import django
django.setup()

import csv
from product.models import ThirdCategory, FirstCategory, SecondCategory

result = []
with open('third_category.csv', mode='r') as third_category:
    reader = csv.reader(third_category)

    for list in reader:
        result.append(list)

for third in result:
    print(third)
    ThirdCategory(
        name               = third[0],
        first_category_id  = third[1],
        second_category_id = third[2]
    ).save()
