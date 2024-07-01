from django.contrib import admin

from .models import UserObjectStorage


class UserObjectStorageAdmin(admin.ModelAdmin):
    class Meta:
        model = UserObjectStorage


admin.site.register(UserObjectStorage, UserObjectStorageAdmin)
