from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Meta:
        db_table = 'accounts_user'  # Указываем явное имя таблицы

    # Добавляем related_name для групп и прав
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='accounts_users',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='accounts_users',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )