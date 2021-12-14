from django.db import models
from django.db.models.fields import TimeField

# Create your models here.

from django.utils import timezone


class TimeModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']


class FAQ(TimeModel):
    content = models.TextField(verbose_name='Content', null=False, blank=False)
    count = models.IntegerField(verbose_name='Count',null=False, blank=False, default=0)
