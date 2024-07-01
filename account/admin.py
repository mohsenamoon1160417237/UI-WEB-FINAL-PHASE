from django.contrib import admin

from .models import MyUser


class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = MyUser


admin.site.register(MyUser, UserAdmin)
