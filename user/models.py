from django.db import models

class User(models.Model):
    login_id        = models.CharField(max_length = 20)
    password        = models.CharField(max_length = 500)
    kakao_id        = models.CharField(max_length = 100, null = True)
    facebook_id     = models.CharField(max_length = 100, null = True)
    twitter_id      = models.CharField(max_length = 100, null = True)
    google_id       = models.CharField(max_length = 100, null = True)
    nickname        = models.CharField(max_length = 20)
    email           = models.EmailField(max_length = 254)
    birthday        = models.DateField(null=True,blank=True)
    gender          = models.CharField(max_length = 10)
    image_url       = models.URLField(max_length = 2000, null = True, blank = True)
    country         = models.CharField(max_length = 100, null = True, blank = True)
    description     = models.CharField(max_length = 500, null = True, blank = True)
    homepage_url    = models.URLField(max_length = 500, null = True, blank = True)
    created_at      = models.DateTimeField(auto_now_add = True)
    updated_at      = models.DateTimeField(auto_now = True)
    follow_relation = models.ManyToManyField('self', through = 'Follower', symmetrical = False)

    class Meta:
        db_table  = 'users'

class Follower(models.Model):
    follower        = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, related_name = 'follower')
    followee        = models.ForeignKey(User, on_delete = models.SET_NULL, null = True,  related_name = 'followee')
    created_at      = models.DateTimeField(auto_now_add = True)

    class Meta:
        unique_together = ('follower', 'followee')
        db_table        = 'followers'

class Point(models.Model):
    user            = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'points')
    plus_point      = models.IntegerField(null = True, blank = True)
    minus_point     = models.IntegerField(null = True, blank = True)
    created_at      = models.DateTimeField(auto_now_add = True)
    updated_at      = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'points'
