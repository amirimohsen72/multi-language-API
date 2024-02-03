from django.contrib import admin
from jalali_date import datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin

from django.contrib.auth.admin import UserAdmin
from core.forms import CustomUserChangeForm, CustomUserCreationForm

from core.mixins import AuthorInAdminMixin
from core.models import CustomUser,  AffiliateRelationModel

from django.contrib.auth import get_user_model
from parler.admin import SortedRelatedFieldListFilter
from parler.admin import TranslatableAdmin

from django.utils.translation import gettext as _

# --------------------------------------custom user ----------------------------------
# --------------------- commission tabular---------
class CommissionInline(admin.TabularInline):
    model = AffiliateRelationModel
    fields = ['marketer', 'type', 'commission', ]
    extra = 0
    fk_name = 'shop'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "marketer":
            kwargs["queryset"] = get_user_model().objects.filter(type='3')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(CustomUser)
class CustomUserAdmin(ModelAdminJalaliMixin, UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    inlines = [CommissionInline]
    list_filter = ("is_staff", "is_superuser", "is_active", "type", "groups")

    # add_form = UserCreationForm
    # form = UserChangeForm
    list_display = ('username', 'fullname', 'is_active', 'is_staff',)
    search_fields = ("username", "fullname", "phone_number")

    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('pesonal info'),
         {'fields': ('fullname', 'phone_number', 'profile_image', 'Address', 'birth_date', 'gender')}),
        (_('user type'),
         {'fields': ('type', 'reff_marketer')}),
    )

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return (
                (_("Account info"), {"fields": ("username", "password")}),
                (_("Personal info"),
                 {"fields": ('fullname', 'phone_number', 'profile_image', 'Address', 'birth_date', 'gender')}),
                (_('user type'), {'fields': ('type', 'reff_marketer',)}),
                (
                    _("Permissions"),
                    {
                        "fields": (
                            "is_active",
                            "is_staff",
                            "is_superuser",
                            "groups",
                            "user_permissions",
                        ),
                    },
                ),
                (_("Important dates"), {"fields": ("last_login", "date_joined")}),
            )
        else:
            return (
                (_("Account info"), {"fields": ("username", "password")}),
                (_("Personal info"),
                 {"fields": ('fullname', 'phone_number', 'profile_image', 'Address', 'birth_date', 'gender')}),
                (_('user type'), {'fields': ('type', 'reff_marketer',)}),
                (
                    _("Permissions"),
                    {
                        "fields": (
                            "is_active",
                        ),
                    },
                ),
                (_("Important dates"), {"fields": ("last_login", "date_joined")}),
            )


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "reff_marketer":
            kwargs["queryset"] = get_user_model().objects.filter(type='3')
            if request.user.type == '3':
                kwargs["queryset"] = get_user_model().objects.filter(type='3', pk=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        if request.user.type == '3':
            initial['reff_marketer'] = request.user
        return initial

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.type == '3':
            return qs.filter(reff_marketer=request.user)
        return qs

