from django.db import models
from taggit.managers import TaggableManager

from apps.core.models import CustomUser


class FoodImage(models.Model):
    image = models.ImageField(upload_to='food_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.image.name


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
    price = models.DecimalField(
        verbose_name='Preço',
        max_digits=10, 
        decimal_places=2,
        null=True,
        blank=True
    )
    food_image = models.ForeignKey(
        to=FoodImage, 
        on_delete=models.CASCADE, 
        related_name='products',
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        to=CustomUser, 
        on_delete=models.CASCADE, 
        related_name='products',
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        return self.name
