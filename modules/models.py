from django.db import models
from config.settings import AUTH_USER_MODEL

NULLABLE = {"null": True, "blank": True}


# Create your models here.
class Module(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Владелец"
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Образовательный модуль"
        verbose_name_plural = "Образовательные модули"
        ordering = ("title",)