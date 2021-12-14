from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ManyToManyField

from backend.app.users.models import User

# Create your models here.


from django.utils import timezone


class TimeModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']


class Personal(models.Model):
    
    name = models.CharField(verbose_name='Name',
                            max_length=255, null=False, blank=False)
    cin = models.CharField(
        verbose_name='Cin', max_length=255, null=False, blank=False)
    email = models.EmailField(verbose_name='Email', null=False, unique=True)
    gsm = models.CharField(verbose_name='GSM', max_length=255,
                           null=False, blank=True, unique=True)

    class Meta:
        abstract = True


class Message(TimeModel):
    """Message for client"""
    body = models.TextField()
    result = models.TextField(default="Hello", blank=True, null=False)
    client = models.ForeignKey(
        User, on_delete=CASCADE, verbose_name="Client", blank=True,  related_name="user")


class Chat(TimeModel):
    """Conversation """
    owner = models.ForeignKey(User, on_delete=CASCADE, verbose_name="owner",
                              blank=True, null=True, related_name="owner")
    messages = ManyToManyField(Message, related_name='messages', blank=True)

    class Meta:
        ordering = ['-updated_at']


class Client(Personal):
    """ AMI user """
    user = models.OneToOneField(
        User, on_delete=models.PROTECT, primary_key=True, null=False)
    chat = models.OneToOneField(
        Chat, on_delete=models.PROTECT, null=True, related_name='chat', blank=True)
