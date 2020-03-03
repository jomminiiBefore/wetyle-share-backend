# -*- coding: utf-8 -*-

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wetyle_share.settings')

import django
django.setup()

import csv
from product.models import FirstCategory

result = []
with open('first_category.csv', mode='r') as first_category:
    reader = csv.reader(first_category)

    for list in reader:
        result.append(list)

for first in result:
    print(first)
    FirstCategory(
        name = first[0]        
    ).save()
