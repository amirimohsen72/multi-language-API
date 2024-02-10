from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField
from parler.models import TranslatableModel, TranslatedFields, TranslationDoesNotExist

from django.contrib.auth import get_user_model
from .category import Category


class Product(TranslatableModel, models.Model):
    TYPE_CHOICES = (
        ('new', _('newest')),
        ('low', _('low level')),
        ('high', _('high level')),
        ('lux', _('luxury')),
    )
    translations = TranslatedFields(
        title=models.CharField(max_length=150, verbose_name=_('title')),
        description=RichTextField(verbose_name=_('description')),
        slug=models.SlugField(max_length=200, unique=True, verbose_name=_('slug'), allow_unicode=True),
        size=models.CharField(max_length=200, verbose_name=_('size'), blank=True),
        price=models.PositiveIntegerField(default=0, verbose_name=_('normal price')),
        weight=models.CharField(max_length=64, verbose_name=_('weight'), help_text=_('example : 1.2 grams'), ),
        carat=models.CharField(max_length=64, verbose_name=_('carat'), help_text=_('example : 24 carats'), ),
        weight_with_wages=models.CharField(max_length=64, verbose_name=_('Weight with wages'),
                                           help_text=_('example : 25 grams'), ),

    )
    category = models.ManyToManyField(Category, related_name="products", verbose_name=_('category'), blank=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                               verbose_name=_('author'),
                               related_name='products', null=True)

    image = models.ImageField(upload_to='product/product_cover/', blank=True, verbose_name=_('product Image'))
    type = models.CharField(choices=TYPE_CHOICES, default='new', max_length=4, verbose_name=_('type'))
    active = models.BooleanField(default=True, verbose_name=_('active'), )
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name=_('create date'))
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name=_('modify date'))

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

    def __str__(self):
        try:
            return self.title
        except TranslationDoesNotExist:
            return self.safe_translation_getter('title', any_language=True)
            # return f'id : {self.id}'

    def category_published(self):
        return self.category.filter(status=True)

    def categories_title(self):
        return ", ".join([category.title for category in self.category_published()])

    categories_title.short_description = _('category')

    @property
    def all_images(self):
        return [{'image': self.image, }] + list(self.gallery.all().only('image', ))

    #
    # def categories_title_published(self):
    #     return ", ".join([category.title for category in self.published_categories])
