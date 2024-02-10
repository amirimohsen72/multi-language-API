from django.contrib import admin
from jalali_date import datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin
from parler.admin import TranslatableAdmin
from django.db.models import Count

from core.mixins import AuthorInAdminMixin
from ..models import NewsModel, CategoryModel, ProductModel, ProductGallery, FavoriteProductModel
from config import settings
from django.contrib.auth import get_user_model

from django.utils.translation import gettext as _


# ----------------------------------------------------------- news -----------------------------------------------------
@admin.register(NewsModel)
class BlogPostAdmin(AuthorInAdminMixin, TranslatableAdmin):
    # pass
    list_display = ('get_title', 'author', 'get_modified_jalali',
                    'status', 'language_column')

    @admin.display(description=_('modified date'), ordering='datetime_modified')
    def get_modified_jalali(self, obj):
        return datetime2jalali(obj.datetime_modified).strftime('%Y/%m/%d %H:%M:%S')

    @admin.display(description=_('title'))
    def get_title(self, obj):
        return obj.safe_translation_getter('title', any_language=True)
