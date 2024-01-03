from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from .managers import CustomUserManager

from django.contrib.auth.models import AbstractUser, Group, Permission  # Agrega la importación de Permission

class CustomUser(AbstractUser):
    # tus campos personalizados aquí

    # Agrega related_name a la relación de permisos de usuario
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name='customuser_user_permissions',  # Agrega este argumento
    )

    # Agrega related_name a la relación de grupos
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='customuser_groups',  # Agrega este argumento
    )

    objects = CustomUserManager()







