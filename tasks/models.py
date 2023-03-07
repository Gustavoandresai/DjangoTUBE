from django.db import models
from django.contrib.auth.models import User


class Data(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    title = models.CharField(max_length=200)
    search = models.CharField(max_length=200)
    link = models.URLField()
    thumbnail = models.URLField(null=True)
    view_count = models.IntegerField(null=True)
    keywords_tags = models.TextField(null=True)
    duration_seconds = models.IntegerField()
    upload_date = models.DateField(null=True)
    published_time = models.CharField(max_length=50, null=True)
    category = models.CharField(max_length=50)
    all_video_description = models.TextField()
    channel = models.CharField(max_length=200)
    subscribers = models.CharField(max_length=50, null=True)
    channel_description = models.TextField(null=True)
    keywords_channel = models.TextField()
    channel_total_views = models.IntegerField(null=True)
    channel_join = models.CharField(max_length=50)
    country = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Credit(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    value = models.IntegerField(default=1000)