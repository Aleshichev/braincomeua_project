"""
Models for storing parser data brain.com.ua
"""

from django.db import models


class Product(models.Model):

    title = models.CharField(
        max_length=255, verbose_name="Product Title", null=True, blank=True
    )
    color = models.CharField(
        max_length=100, verbose_name="Color", null=True, blank=True
    )
    memory = models.CharField(
        max_length=100, verbose_name="Memory Capacity", null=True, blank=True
    )
    manufacturer = models.CharField(
        max_length=100, verbose_name="Manufacturer", null=True, blank=True
    )
    regular_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Regular Price",
        null=True,
        blank=True,
    )
    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Sale Price",
        null=True,
        blank=True,
    )
    photos = models.JSONField(verbose_name="Product Photos", null=True, blank=True)
    code = models.CharField(
        max_length=100, verbose_name="Product Code", null=True, blank=True
    )
    review_count = models.IntegerField(
        verbose_name="Review Count", null=True, blank=True
    )
    screen_diagonal = models.CharField(
        max_length=100, verbose_name="Diagonal", null=True, blank=True
    )
    screen_resolution = models.CharField(
        max_length=100, verbose_name="Screen Resolution", null=True, blank=True
    )
    specifications = models.JSONField(
        verbose_name="Specifications", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")

    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update Date")

    class Meta:
        db_table = "products"
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.title} - {self.code}"
