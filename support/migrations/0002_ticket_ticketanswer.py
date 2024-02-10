# Generated by Django 4.2.6 on 2023-11-14 06:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('support', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, verbose_name='message text')),
                ('attachment', models.FileField(blank=True, help_text='you can upload image or *.zip file for attachment.', upload_to='tickets/messages/', verbose_name='attachment file')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='create time')),
                ('datetime_modified', models.DateTimeField(auto_now=True, verbose_name='modify time')),
                ('readed', models.BooleanField(default=False, verbose_name='readed')),
                ('status', models.CharField(choices=[('0', 'new from user'), ('1', 'seen user message'), ('2', 'new from admin'), ('3', 'seen admin message'), ('4', 'spam')], max_length=3, verbose_name='status')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_ticket', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'ticket',
                'verbose_name_plural': 'tickets',
                'ordering': ['readed', '-datetime_created'],
            },
        ),
        migrations.CreateModel(
            name='TicketAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, verbose_name='message text')),
                ('attachment', models.FileField(blank=True, help_text='you can upload image or *.zip file for attachment.', upload_to='tickets/messages/answers/', verbose_name='attachment file')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='create time')),
                ('datetime_modified', models.DateTimeField(auto_now=True, verbose_name='modify time')),
                ('admin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='admin_ticket_answer', to=settings.AUTH_USER_MODEL, verbose_name='admin')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='support.ticket')),
            ],
        ),
    ]