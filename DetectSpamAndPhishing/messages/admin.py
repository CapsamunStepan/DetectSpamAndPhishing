from django.contrib import admin
from .models import GmailUser, GmailMessage


# Register your models here.
@admin.register(GmailUser)
class GmailUserAdmin(admin.ModelAdmin):
    list_display = ('gmail', 'total_messages')


@admin.register(GmailMessage)
class GmailMessageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in GmailMessage._meta.fields]
