from django.contrib import admin
from jalali_date import datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin
from parler.admin import TranslatableAdmin
from django.db.models import Count

from core.mixins import AuthorInAdminMixin
from ..models import NewsModel, CategoryModel, ProductModel, ProductGallery,  FavoriteProductModel
from config import settings
from django.contrib.auth import get_user_model

from django.utils.translation import gettext as _


 

# ---------------------------------------------------- product category ------------------------------------------------
@admin.register(CategoryModel)
class ProductCategoryAdmin(TranslatableAdmin):
    list_display = ('get_title', 'status', 'sort', 'language_column')

    def get_prepopulated_fields(self, request, obj=None):
        return {
            'slug': ('title',)
        }

    @admin.display(description=_('title'))
    def get_title(self, obj):
        return obj.safe_translation_getter('title', any_language=True)
  