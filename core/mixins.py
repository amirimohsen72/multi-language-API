from django.contrib import admin
from django.contrib.auth import get_user_model

class AuthorInAdminMixin():

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            if request.user.is_superuser:
                kwargs["queryset"] = get_user_model().objects.filter(is_staff=True)
            else:
                kwargs["queryset"] = get_user_model().objects.filter(pk=request.user.pk)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial['author'] = request.user
        return initial

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    # -------
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == "author":
    #         if request.user.is_superuser:
    #             kwargs["queryset"] = get_user_model().objects.filter(is_staff=True)
    #         else:
    #             kwargs["queryset"] = get_user_model().objects.filter(pk=request.user.pk)
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)
    #
    # def get_changeform_initial_data(self, request):
    #     initial = super(FaqAdmin, self).get_changeform_initial_data(request)
    #     initial['author'] = request.user
    #     return initial
    #
    # def get_queryset(self, request):
    #     if request.user.is_superuser:
    #         return Faq.objects.all()
    #     else:
    #         return Faq.objects.filter(author=request.user.pk)