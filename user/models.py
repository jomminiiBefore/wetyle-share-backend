from django.db import models

class User(models.Model):

    login_id    = models.CharField(max_length = 20)
    password    = models.CharField(max_length = 500)
    kakao_id    = models.CharField(max_length = 100, null = True)
    facebook_id = models.CharField(max_length = 100, null = True)
    twitter_id  = models.CharField(max_length = 100, null = True)
    google_id   = models.CharField(max_length = 100, null = True)
    nickname    = models.CharField(max_length = 20)
    email       = models.CharField(max_length = 200)
    birthday    = models.DateField(null=True,blank=True)
    gender      = models.CharField(max_length = 10)
    image       = models.URLField(max_length = 500, null = True, blank = True)
    country     = models.CharField(max_length = 100, null = True,  blank = True)
    description = models.CharField(max_length = 500, null = True, blank = True)
    url         = models.CharField(max_length = 200, null = True, blank = True)
    created_at  = models.DateTimeField(auto_now_add = True)
    updated_at  = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'users'


