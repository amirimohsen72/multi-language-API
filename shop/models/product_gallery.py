from django.db import models
from django.utils.translation import gettext_lazy as _

from .product import Product


class ProductGallery(models.Model):
    class Meta:
        verbose_name = _('product gallery')
        verbose_name_plural = _('product galleries')

    title = models.CharField(max_length=150, verbose_name=_('title'),blank=True, )

    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name=_('product'),
                                related_name='gallery', null=True)
    image = models.ImageField(upload_to='product/gallery/', blank=True, verbose_name=_('product Image'))
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name=_('modify date'))

    def __str__(self):
        if self.product:
            return f'product:{self.product.pk} - {self.title[0:30]} '
        else:
            return f'{self.pk} {self.title}'
