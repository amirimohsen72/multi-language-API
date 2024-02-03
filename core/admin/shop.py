from django.contrib import admin
from jalali_date import datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin

from django.contrib.auth.admin import UserAdmin
from core.forms import CustomUserChangeForm, CustomUserCreationForm

from core.mixins import AuthorInAdminMixin
from core.models import CustomUser, ShopUserDetailModel, AffiliateRelationModel

from django.contrib.auth import get_user_model
from parler.admin import SortedRelatedFieldListFilter
from parler.admin import TranslatableAdmin

from django.utils.translation import gettext as _

 
# -------------------------------------------------- shop user --------------------------------------------
@admin.register(ShopUserDetailModel)
class ShopDetailAdmin(TranslatableAdmin):
    list_display = ('user', 'get_title', 'user_fullname', 'language_column')
    search_fields = ['user__username', 'user__fullname', 'translations__title', ]

    @admin.display(description=_('title'))
    def get_title(self, obj):
        return obj.safe_translation_getter('title', any_language=True)

    @admin.display(description=_('fullname'))
    def user_fullname(self, obj):
        return obj.user.fullname

    def get_readonly_fields(self, request, obj=None):
        if obj:  # obj is not None, so this is an edit
            return ['user', 'user_license', ]  # Return a list or tuple of readonly fields' names
        else:  # This is an addition
            return []

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
 
# -------------------------------------------------- shop commissions --------------------------------------------
@admin.register(AffiliateRelationModel)
class ShopCommissionAdmin(admin.ModelAdmin):
    list_display = ('marketer', 'shop',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "shop":
            kwargs["queryset"] = get_user_model().objects.filter(type='2')
        if db_field.name == "marketer":
            kwargs["queryset"] = get_user_model().objects.filter(type='3')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial['shop'] = request.user
        return initial
