from django.contrib import admin
from jalali_date import datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin

from django.contrib.auth.admin import UserAdmin
from core.forms import CustomUserChangeForm, CustomUserCreationForm

from core.mixins import AuthorInAdminMixin
from core.models import SiteSettingModel, LanguageModel

from django.contrib.auth import get_user_model
from parler.admin import SortedRelatedFieldListFilter
from parler.admin import TranslatableAdmin

from django.utils.translation import gettext as _

admin.site.site_header = _('site panel - multi language api')


  
# -------------------------------------------------- setting site --------------------------------------------
@admin.register(SiteSettingModel)
class SettingAdmin(TranslatableAdmin):
    list_display = ('title', 'sort', 'status',)


# -------------------------------------------------- setting site --------------------------------------------
# @admin.register(Language)
# class LanguageAdmin(admin.ModelAdmin):
#     list_display = ('title', 'lang_code', 'sort',)
#     search_fields = ('title', 'lang_code',)
#     # list_filter = ('status',)

 