from django_filters.rest_framework import FilterSet
import django_filters
from django.db.models import Q

from .models import ProductModel


class ProductFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method='my_custom_filter', label="Search")
    LANG_CHOICES = [
        ('fa', 'Farsi'),
        ('en', 'English'),
        ('ar', 'Arabic'),
        ('tr', 'Turkish'),
    ]
    lang = django_filters.ChoiceFilter(choices=LANG_CHOICES, label="language", method='language_filter', )
    license_key = django_filters.UUIDFilter(label="license key", method='license_filter', )

    class Meta:
        model = ProductModel
        fields = {'category', 'type', 'brand', }

    def language_filter(self, queryset, name, value):
        # if value in HomeSearchFilter.LANG_CHOICES:
        #     lang = self.request.value.get('lang', 'en')
        #     queryset = queryset.translated(lang)
        return queryset

    def license_filter(self, queryset, name, value):
        if value:
            queryset = queryset.filter(author__shop_detail__user_license=value)
        return queryset

    def my_custom_filter(self, queryset, name, value):
        # queryset = queryset.translated(title=search)
        queryset = queryset.filter(translations__title__icontains=value)
        return queryset


class HomeSearchFilter(django_filters.FilterSet):
    LANG_CHOICES = [
        ('fa', 'Farsi'),
        ('en', 'English'),
        ('ar', 'Arabic'),
        ('tr', 'Turkish'),
    ]
    lang = django_filters.ChoiceFilter(choices=LANG_CHOICES, label="language", )
    search = django_filters.CharFilter(label="Search")
    license_key = django_filters.UUIDFilter(label="license key")

    class Meta:
        model = ProductModel
        fields = {'category', }

    # def language_filter(self, queryset, name, value):
    #     # queryset = queryset.translated(title=search)
    #     print(value)
    #     queryset = queryset.translated(value)
    #
    #     if value in HomeSearchFilter.LANG_CHOICES:
    #         queryset = queryset.translated(value)
    #         print(queryset.query)
    #     return queryset

    # def my_custom_filter(self, queryset, name, value):
    #     # queryset = queryset.translated(title=search)
    #     queryset = queryset.filter(translations__title__icontains=value)
    #     return queryset


class HomeProductFilter(django_filters.FilterSet):
    LANG_CHOICES = [
        ('fa', 'Farsi'),
        ('en', 'English'),
        ('ar', 'Arabic'),
        ('tr', 'Turkish'),
    ]
    lang = django_filters.ChoiceFilter(choices=LANG_CHOICES, label="language", )
    # license_key = django_filters.UUIDFilter(label="license key")
