from django.contrib import admin
from .models import Message, Chat, Client
# Register your models here.


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('body', 'client', "result")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'chat',)


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('owner',)
