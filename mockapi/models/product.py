from django.core.files.storage import FileSystemStorage
from django.db import models
from django.urls import reverse

from mockapi.models.attributes import Tag, Color


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            self.delete(name)
        return name


def product_image_path(instance):
    return f'product/{instance.pk}.webp'


class Product(models.Model):
    title = models.CharField(max_length=150, default='Product')
    description = models.TextField(blank=True)
    # image_url = models.TextField(blank=True)
    image_url = models.ImageField(
        default='product/default.jpg',
        upload_to=product_image_path,
        storage=OverwriteStorage()
    )
    # categories = models.ManyToManyField(Category, related_name='products', blank=True)
    black_price = models.FloatField(blank=True, default=12000)
    final_price = models.FloatField(default=10000)
    quantity = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField(Tag, related_name='products', blank=True)
    colors = models.ManyToManyField(Color, related_name='products', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        # ordering = ['pk', 'title']
