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


# ------------------------------------------------------- products -----------------------------------------------------

# --------------------------product gallery iinline -----
class ProductGalleryInline(admin.TabularInline):
    # class OrderItemInline(admin.StackedInline):
    model = ProductGallery
    fields = ['title', 'image', ]
    extra = 0  # برای درج مستقیم رکورد جدید

# ---------------------------product----------------------
@admin.register(ProductModel)
class ProductAdmin(AuthorInAdminMixin, TranslatableAdmin):
    list_display = ('get_title', 'categories_title', 'author', 'get_modified_jalali', 'active', 'language_column')
    inlines = [ProductGalleryInline,  ]

    def get_prepopulated_fields(self, request, obj=None):
        return {
            'slug': ('title',)
        }

    @admin.display(description=_('modified date'), ordering='datetime_modified')
    def get_modified_jalali(self, obj):
        return datetime2jalali(obj.datetime_modified).strftime('%Y/%m/%d %H:%M:%S')

    @admin.display(description=_('title'))
    def get_title(self, obj):
        return obj.safe_translation_getter('title', any_language=True)



