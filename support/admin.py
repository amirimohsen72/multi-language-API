from django.contrib import admin
from jalali_date import datetime2jalali

from core.mixins import AuthorInAdminMixin
from .models import QuestionModel, TicketMessageModel, TicketAnswerModel
from django.contrib.auth import get_user_model

from django.utils.translation import gettext as _

from parler.admin import TranslatableAdmin


# ------------------------------------------------------ question ------------------------------------------------
@admin.register(QuestionModel)
class QuestionAdmin(AuthorInAdminMixin, TranslatableAdmin):
    list_display = ('get_title', 'author', 'get_modified_jalali', 'status', 'language_column')

    @admin.display(description=_('modified date'), ordering='datetime_modified')
    def get_modified_jalali(self, obj):
        return datetime2jalali(obj.datetime_modified).strftime('%Y/%m/%d %H:%M:%S')

    @admin.display(description=_('title'))
    def get_title(self, obj):
        return obj.safe_translation_getter('title', any_language=True)


# -------------------------------------------------------ticket messages ------------------------------------------


class TicketChildInline(admin.TabularInline):
    model = TicketAnswerModel

    # class Media:
    #     css = {
    #         'all': ('system/admin_style.css',)
    #     }

    fields = ['admin', 'message', 'attachment', ]
    extra = 0  # برای درج مستقیم رکورد جدید

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "admin":

            if request.user.is_superuser:
                kwargs["queryset"] = get_user_model().objects.filter(is_staff=True)
            else:
                kwargs["queryset"] = get_user_model().objects.filter(pk=request.user.pk)
            kwargs["initial"] = request.user
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(TicketMessageModel)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('message', 'user', 'get_modified_jalali', 'readed', 'status')
    inlines = [TicketChildInline, ]
    list_filter = ('status',)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # obj is not None, so this is an edit
            return ['user', ]  # Return a list or tuple of readonly fields' names
        else:  # This is an addition
            return []

    @admin.display(description=_('modified date'), ordering='datetime_modified')
    def get_modified_jalali(self, obj):
        return datetime2jalali(obj.datetime_modified).strftime('%Y/%m/%d %H:%M:%S')

    def change_view(self, request, object_id, extra_context=None):
        ticket = self.get_object(request, object_id)
        ticket.readed = True
        if ticket.status == '0':
            ticket.status = '1'
        ticket.save()

        return super(TicketAdmin, self).change_view(request, object_id)
