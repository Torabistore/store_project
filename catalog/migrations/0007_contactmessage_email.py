# Generated by Django 5.2.3 on 2025-07-11 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_contactmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactmessage',
            name='email',
            field=models.EmailField(blank=True, max_length=255, verbose_name='ایمیل'),
        ),
    ]
