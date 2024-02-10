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
    
# ---------------------------------------------------- favorite products ---------------------------------------------

@admin.register(FavoriteProductModel)
class FavoriteProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'is_active', ]
    # autocomplete_fields = ["product", ]

