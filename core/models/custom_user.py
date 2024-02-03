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




# ------------------------------------------ custom user ----------------------------------------------
class CustomUser(AbstractUser):
    class Meta:
        verbose_name = _('account')
        verbose_name_plural = _('accounts')

    Gender_CHOICES = (
        ('m', _('man')),
        ('f', _('woman')),
    )
    TYPE_CHOICES = (
        ('1', _('normal user')),
        ('2', _('shop')),
        ('3', _('marketer')),
    )

    username = models.CharField(
        _("national code"), max_length=10, unique=True,
        help_text=_(
            "personal national id of user"
        ),
        error_messages={
            "unique": _("A user with that national code already exists."),
        },
    )
    first_name = None
    last_name = None

    fullname = models.CharField(max_length=128, null=True, verbose_name=_('full name'))
    phone_number = models.CharField(max_length=15, null=True, verbose_name=_('phone number'))
    profile_image = models.ImageField(upload_to='customer/profile/', blank=True, verbose_name=_('Profile Image'),
                                      help_text=_('only image file'))
    # national_code = models.CharField(max_length=10, blank=True, verbose_name=_('national code'), unique=True, )
    confirm_code = models.CharField(max_length=5, null=True, )
    confirm_req_time = models.DateTimeField(null=True, blank=True, )
    Address = models.TextField(blank=True, verbose_name=_('address'))
    gender = models.CharField(choices=Gender_CHOICES, max_length=2, verbose_name=_('gender'), default='m')
    type = models.CharField(choices=TYPE_CHOICES, max_length=2, verbose_name=_('account type'), default='1',
                            help_text='1 user , 2 shop , 3 marketer')
    birth_date = models.DateField(null=True, blank=True, verbose_name=_('birth date'))

    reff_marketer = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,
                                         verbose_name=_('referral marketer'),
                                         related_name='customers', )

    def __str__(self):
        if self.fullname:
            return self.fullname
        else:
            return self.username

    def get_full_name(self):
        """
        Return the fullname. rerwited .
        """
        return self.fullname


# -------------------------------------------------- shoper user detail ------------------------------------
class ShopUserDetail(TranslatableModel, models.Model):
    class Meta:
        verbose_name = _('shoper user detail')
        verbose_name_plural = _('shoper users detail')
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['user_license']),
        ]

    user = models.OneToOneField(get_user_model(), on_delete=models.PROTECT, primary_key=True, verbose_name=_('user'),
                                related_name='shop_detail', )
    user_license = models.UUIDField(default=uuid4, verbose_name=_('user license key'), unique=True)

    translations = TranslatedFields(
        title=models.CharField(max_length=200, verbose_name=_('title'), null=True),
        app_logo=models.ImageField(upload_to='setting/shops/logos/', blank=True,
                                   verbose_name=_('app logo'), help_text=_('logo for application')),

        footer_description=RichTextField(blank=True, null=True, verbose_name=_('description in footer')),
        about_gandom=RichTextField(blank=True, null=True, verbose_name=_('about gandom')),

        instagram=models.CharField(max_length=200, verbose_name=_('instagram'), blank=True),
        mobile=models.CharField(max_length=200, verbose_name=_('mobile'), blank=True),
        tel_phone=models.CharField(max_length=200, verbose_name=_('telephone'), blank=True),
        support_phone=models.CharField(max_length=200, verbose_name=_('support phone'), blank=True),
        email=models.CharField(max_length=200, verbose_name=_('email'), blank=True),
    )

    # status = models.BooleanField(default=True, verbose_name=_('status'))

    def __str__(self, ):
        return self.user.fullname
        # try:
        #     return self.title
        # except TranslationDoesNotExist:
        # return self.safe_translation_getter('title', any_language=True)

    def __unicode__(self):
        return self.title
