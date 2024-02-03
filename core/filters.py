import django_filters


class PublicFilter(django_filters.FilterSet):
    LANG_CHOICES = [
        ('fa', 'Farsi'),
        ('en', 'English'),
        ('ar', 'Arabic'),
        ('tr', 'Turkish'),
    ]
    lang = django_filters.ChoiceFilter(choices=LANG_CHOICES, label="language", )
    license_key = django_filters.UUIDFilter(label="license key", method='license_filter', )

    def license_filter(self, queryset, name, value):
        # if value:
        #     queryset = queryset.filter(author__shop_detail__user_license=value)
        return queryset
