from django.contrib import admin
from . import models

class EntryAdmin(admin.ModelAdmin):
    list_display = ['title','author','visitors','created_time','modifyed_time']

@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'occupation', 'gender', 'birthday']
    list_filter = ['gender', 'city']

admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Entry,EntryAdmin)