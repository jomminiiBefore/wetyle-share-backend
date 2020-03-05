# -*- coding: utf-8 -*-

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wetyle_share.settings')

import django
django.setup()

import csv
from user.models    import *
from card.models    import *
from product.models import *

def add_style_related_item():
    with open('./upload/style_related_item - style.csv', mode='r') as style_related_item_lists:
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

