from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField
from parler.models import TranslatableModel, TranslatedFields

from django.contrib.auth import get_user_model


class Category(TranslatableModel, models.Model):
    translations = TranslatedFields(
        title=models.CharField(max_length=200, verbose_name=_('title')),
        description=RichTextField(verbose_name=_('description')),
        slug=models.SlugField(max_length=200, unique=True, verbose_name=_('slug'), allow_unicode=True),
    )

    cover = models.ImageField(upload_to='products/category/', blank=True,
                              verbose_name=_('cover image'))
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL,
                               related_name='children', verbose_name=_('parent category'))

    status = models.BooleanField(default=True, verbose_name=_('status'))
    sort = models.PositiveSmallIntegerField(default=1, verbose_name=_('sort'))

    class Meta:
        verbose_name = _('product category')
        verbose_name_plural = _('products categories')

    def __str__(self):
        return self.title
