# -*- coding: utf-8 -*-

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wetyle_share.settings')

import django
django.setup()

import csv
from user.models import User
from card.models import Collection, Style, StyleComment, StyleRelatedItem

# User
with open('./upload/user.csv', mode='r') as user_lists:
    reader = csv.reader(user_lists, delimiter=',')

    for user in list(reader)[1:]:
        print(user)
        User(
            login_id = user[0],
            password = user[1],
            nickname = user[2],
            gender = user[3],
            email = user[4],
        ).save()

# Collection
with open('./upload/collection.csv', mode='r') as collection_lists:
    reader = csv.reader(collection_lists, delimiter=',')

    for collection in list(reader)[1:]:
        print(collection)
        Collection(
            name = collection[0],
            description = collection[1],
            user_id = collection[2],
        ).save()

# Style
with open('./upload/style.csv', mode='r') as style_lists:
    reader = csv.reader(style_lists, delimiter=',')

    for style in list(reader)[1:]:
        print(style)
        Style(
            description = style[0],
            image_url = style[1],
            user_id = style[2],
        ).save()

# StyleComment
with open('./upload/style_comment.csv', mode='r') as style_comment_lists:
    reader = csv.reader(style_comment_lists, delimiter=',')

    for comment in list(reader)[1:]:
        StyleComment(
            description = comment[0],
            style_id = comment[1],
            user_id = comment[2],
        ).save()

# StyleRelatedItem
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

# StyleLike
with open('./upload/style_like.csv', mode='r') as style_like_lists:
    reader = csv.reader(style_like_lists, delimiter=',')

    for item in list(reader)[1:]:
        StyleLike(
            style_id  = item[0],
            user_id   = item[1],
        ).save()

