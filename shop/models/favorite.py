from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from . import ProductModel


class FavoriteProduct(models.Model):
    class Meta:
        verbose_name = _('favorite')
        verbose_name_plural = _('favorite products')
        index_together = ['product', 'user', ]
        unique_together = ['product', 'user', ]

    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='favorite',
                                verbose_name=_('product'))
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             verbose_name=_('user'),
                             related_name='favorite_product', )
    is_active = models.BooleanField(default=True, verbose_name=_('active'))
