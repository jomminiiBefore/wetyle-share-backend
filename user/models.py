from core.models import TimeStampedModel

from django.db import models

class User(TimeStampedModel):

    """ User Model Definition """

    login_id  = models.CharField(max_length = 20)
    password  = models.CharField(max_length = 500)
    kakao_id  = models.CharField(max_length = 100, null = True)
    fb_id     = models.CharField(max_length = 100, null = True)
    twt_id    = models.CharField(max_length = 100, null = True)
    gg_id     = models.CharField(max_length = 100, null = True)
    nickname  = models.CharField(max_length = 20)
    email     = models.CharField(max_length = 200)
    birthday  = models.DateField(null=True,blank=True)
    sex       = models.CharField(max_length = 10)
    image     = models.URLField(max_length = 500, null = True, blank = True)
    country   = models.CharField(max_length = 100, null = True,  blank = True)
    desc      = models.CharField(max_length = 500, null = True, blank = True)
    url       = models.CharField(max_length = 200, null = True, blank = True)

    class Meta:
        db_table = 'users'


