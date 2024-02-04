from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField
from parler.models import TranslatableModel, TranslatedFields

from django.contrib.auth import get_user_model


class Question(TranslatableModel, models.Model):
    STATUS_CHOICES = (
        ('0', _('draft')),
        ('1', _('published')),

    )

    translations = TranslatedFields(
        title=models.CharField(max_length=200, verbose_name=_('title')),
        description=RichTextField(verbose_name=_('description')),
    )
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                               verbose_name=_('author'),
                               related_name='question_author', null=True)
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('create time'))
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name=_('modify time'))
    sort = models.PositiveSmallIntegerField(default=1, verbose_name=_('sort number'))

    status = models.CharField(choices=STATUS_CHOICES, max_length=3, verbose_name=_('status'))

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')

    def __str__(self):
        return self.title
