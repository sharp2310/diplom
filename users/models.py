from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"null": True, "blank": True}


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="почта")
    phone = models.CharField(max_length=35, verbose_name="телефон", **NULLABLE)
    avatar = models.ImageField(
        upload_to="users/", verbose_name="аватар", **NULLABLE
    )
    is_active = models.BooleanField(default=False, verbose_name="активен")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        ordering = ("email",)