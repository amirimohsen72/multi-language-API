from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField
from parler.models import TranslatableModel, TranslatedFields

from django.contrib.auth import get_user_model


class Ticket(models.Model):
    class Meta:
        verbose_name = _('ticket')
        verbose_name_plural = _('tickets')
        ordering = ['readed', '-datetime_created', ]

    STATUS_CHOICES = (
        ('0', _('new from user')),
        ('1', _('seen user message')),
        ('2', _('new from admin')),
        ('3', _('admin message seen by user')),
        ('4', _('spam')),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             verbose_name=_('user'),
                             related_name='user_ticket', null=True)


    message = models.TextField(verbose_name=_('message text'), blank=True)
    attachment = models.FileField(upload_to='tickets/messages/customer_file/', blank=True,
                                  verbose_name=_('attachment file'),
                                  help_text=_('you can upload image or *.zip file for attachment.'))

    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('create time'))
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name=_('modify time'))
    readed = models.BooleanField(default=False, verbose_name=_('readed'), )

    status = models.CharField(choices=STATUS_CHOICES, default='0', max_length=3, verbose_name=_('status'))

    def __str__(self):
        try:
            if self.user.get_full_name():
                return f'{self.user.get_full_name()[0:40]} .:. {self.message[0:25]}'
            if self.user.username:
                return f'{self.user.username[0:40]} .:. {self.message[0:25]}'
        except:
            return f'{self.message[0:25]}'


class TicketAnswer(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='answers')
    admin = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, verbose_name=_('admin'),
                              related_name='admin_ticket_answer', null=True)
    message = models.TextField(verbose_name=_('message text'), blank=True)
    attachment = models.FileField(upload_to='tickets/messages/answers/', blank=True,
                                  verbose_name=_('attachment file'),
                                  help_text=_('you can upload image or *.zip file for attachment.'))
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('create time'))
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name=_('modify time'))

    def __str__(self):
        return f'Answer for Ticket: {self.ticket.id}'
