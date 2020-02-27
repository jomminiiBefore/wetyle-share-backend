from django.db import models

class Brand(models.Model):
    name            = models.CharField(max_length = 50)
    small_image_url = models.URLField(max_length = 2000)
    large_image_url = models.URLField(max_length = 2000)
    description     = models.CharField(max_length = 500, blank = True)
    created_at      = models.DateTimeField(auto_now_add = True)
    updated_at      = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = 'brands'
