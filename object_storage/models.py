from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import MyUser


class UserObjectStorage(models.Model):
    file_name = models.CharField(
        max_length=500,
        verbose_name=_("file_name"),
    )
    file_size = models.BigIntegerField(
        verbose_name=_("file_size")
    )
    uploaded_date_time = models.DateTimeField(
        verbose_name=_("uploaded_date_time"),
        auto_now_add=True
    )
    user = models.ForeignKey(  # Owner
        to='account.MyUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='object_storages',
        verbose_name=_("user")
    )
    users_added = models.ManyToManyField(  # Users that owner add
        to='account.MyUser',
        verbose_name=_("users_added")
    )

    def get_file_name_extension(self) -> str:
        return self.file_name.split(".")[-1]
