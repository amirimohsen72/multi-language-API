# Generated by Django 5.0.1 on 2024-02-10 07:57

import ckeditor.fields
import django.db.models.deletion
import parler.fields
import parler.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover', models.ImageField(blank=True, upload_to='products/category/', verbose_name='cover image')),
                ('status', models.BooleanField(default=True, verbose_name='status')),
                ('sort', models.PositiveSmallIntegerField(default=1, verbose_name='sort')),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='shop.category', verbose_name='parent category')),
            ],
            options={
                'verbose_name': 'product category',
                'verbose_name_plural': 'products categories',
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover', models.ImageField(blank=True, upload_to='news/cover/', verbose_name='cover image')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='create time')),
                ('datetime_modified', models.DateTimeField(auto_now=True, verbose_name='modify time')),
                ('status', models.CharField(choices=[('0', 'draft'), ('1', 'published'), ('2', 'unallowable')], max_length=3, verbose_name='status')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='news', to=settings.AUTH_USER_MODEL, verbose_name='author')),
            ],
            options={
                'verbose_name': 'the news',
                'verbose_name_plural': 'News',
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='product/product_cover/', verbose_name='product Image')),
                ('type', models.CharField(choices=[('new', 'newest'), ('low', 'low level'), ('high', 'high level'), ('lux', 'luxury')], default='new', max_length=4, verbose_name='type')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='create date')),
                ('datetime_modified', models.DateTimeField(auto_now=True, verbose_name='modify date')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('category', models.ManyToManyField(blank=True, related_name='products', to='shop.category', verbose_name='category')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ProductGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=150, verbose_name='title')),
                ('image', models.ImageField(blank=True, upload_to='product/gallery/', verbose_name='product Image')),
                ('datetime_modified', models.DateTimeField(auto_now=True, verbose_name='modify date')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gallery', to='shop.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'product gallery',
                'verbose_name_plural': 'product galleries',
            },
        ),
        migrations.CreateModel(
            name='CategoryTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('description', ckeditor.fields.RichTextField(verbose_name='description')),
                ('slug', models.SlugField(allow_unicode=True, max_length=200, unique=True, verbose_name='slug')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='shop.category')),
            ],
            options={
                'verbose_name': 'product category Translation',
                'db_table': 'shop_category_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='NewsTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('description', ckeditor.fields.RichTextField(verbose_name='description')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='shop.news')),
            ],
            options={
                'verbose_name': 'the news Translation',
                'db_table': 'shop_news_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='FavoriteProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_product', to=settings.AUTH_USER_MODEL, verbose_name='user')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to='shop.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'favorite',
                'verbose_name_plural': 'favorite products',
                'unique_together': {('product', 'user')},
                'index_together': {('product', 'user')},
            },
        ),
        migrations.CreateModel(
            name='ProductTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.CharField(max_length=150, verbose_name='title')),
                ('description', ckeditor.fields.RichTextField(verbose_name='description')),
                ('slug', models.SlugField(allow_unicode=True, max_length=200, unique=True, verbose_name='slug')),
                ('size', models.CharField(blank=True, max_length=200, verbose_name='size')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='normal price')),
                ('weight', models.CharField(help_text='example : 1.2 grams', max_length=64, verbose_name='weight')),
                ('carat', models.CharField(help_text='example : 24 carats', max_length=64, verbose_name='carat')),
                ('weight_with_wages', models.CharField(help_text='example : 25 grams', max_length=64, verbose_name='Weight with wages')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='shop.product')),
            ],
            options={
                'verbose_name': 'product Translation',
                'db_table': 'shop_product_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]
