from uuid import uuid4

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

# 3th party
from ckeditor.fields import RichTextField
from translated_fields import TranslatedField
from parler.models import TranslatableModel, TranslatedFields, TranslationDoesNotExist


# ------------------------------------------ affiliate shop and marketer ----------------------------
class AffiliateRelation(models.Model):
    class Meta:
        verbose_name = _('Marketer Affiliate Relation')
        verbose_name_plural = _('Marketer Affiliate Relations')
        unique_together = [['marketer', 'shop']]

    TYPE_CHOICES = (
        ('1', _('add')),
        ('2', _('percent')),
    )
    marketer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='affiliate_relations',
                                 verbose_name=_('marketer'), )
    shop = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='seller_relations',
                             verbose_name=_('shop'))
    commission = models.IntegerField(default=0, verbose_name=_('commission'),
                                     help_text=_('Enter as an integer . like 10 ( % or + ) '))
    type = models.CharField(choices=TYPE_CHOICES, max_length=2, verbose_name=_('commission type'), default='1', )
