from django.db import models
from taggit.managers import TaggableManager


class Products(models.Model):
    category = TaggableManager(
        verbose_name='Categoria',
        blank=True
    )
    name = models.CharField(
        verbose_name='Nome',
        max_length=255
    )
    description = models.TextField(
        verbose_name='Descrição',
        max_length=2500
    )
