import re

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class MyUser(AbstractUser):
    username = models.CharField(
        verbose_name=_("username"),
        unique=True,
        validators=[
            MinLengthValidator(4),
            RegexValidator(
                regex=r'^[a-z\s]+$',
                message='Please Enter valid English character',
                flags=re.IGNORECASE
            )
        ],
        max_length=500
    )
    email = models.EmailField(
        verbose_name=_('email'),
        unique=True
    )
    password = models.CharField(
        verbose_name=_("password"),
        max_length=128,
        validators=[
            MinLengthValidator(6, message="The field must contain at least 6 characters"),
            RegexValidator(
                regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).+$',
                message='Password must contain at least one lower case letter, one upper case letter, and one special'
                        'character',
                flags=0
            )
        ]
    )
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
