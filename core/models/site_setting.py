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


# Create your models here.



# ---------------------------------------------------- languages -------------------------------------------

class Language(models.Model):
    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')
        ordering = ['-sort', ]

    title = models.CharField(max_length=200, verbose_name=_('title'))
    lang_code = models.CharField(max_length=24, verbose_name=_('language code'))
    lang_logo = models.ImageField(upload_to='setting/lang/', blank=True,
                                  verbose_name=_('language logo'), help_text=_('language for application'))
    sort = models.SmallIntegerField(default=1, verbose_name=_('sort'))

    def __str__(self):
        return self.title


# ---------------------------------------------------- site setting -----------------------------------------

# class LastSettingManager(models.Manager):
#     def active(self):
#         return self.filter(status=True).order_by('sort').first()


class SiteSetting(TranslatableModel, models.Model):
    class Meta:
        verbose_name = _('Site Setting')
        verbose_name_plural = _('Site Settings')

    favicon = models.ImageField(upload_to='setting/favicon/', blank=True,
                                verbose_name=_('favicon'))
    translations = TranslatedFields(
        title=models.CharField(max_length=200, verbose_name=_('title')),
        site_logo=models.ImageField(upload_to='setting/logos/', blank=True,
                                    verbose_name=_('site logo'), help_text=_('logo for application')),

        footer_description=RichTextField(blank=True, null=True, verbose_name=_('description in footer')),
        about_gandom=RichTextField(blank=True, null=True, verbose_name=_('about gandom')),

        instagram=models.CharField(max_length=200, verbose_name=_('instagram'), blank=True),
        mobile=models.CharField(max_length=200, verbose_name=_('mobile'), blank=True),
        tel_phone=models.CharField(max_length=200, verbose_name=_('telephone'), blank=True),
        support_phone=models.CharField(max_length=200, verbose_name=_('support phone'), blank=True),
        email=models.CharField(max_length=200, verbose_name=_('email'), blank=True),
        telegram=models.CharField(max_length=200, verbose_name=_('telegram url'), null=True, blank=True),
    )
    sort = models.SmallIntegerField(default=1, verbose_name=_('sort'))
    status = models.BooleanField(default=True, verbose_name=_('status'))

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title
    # objects = LastSettingManager()

