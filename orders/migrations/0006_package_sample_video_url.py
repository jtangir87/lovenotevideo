# Generated by Django 2.2.10 on 2020-06-23 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_eventcoupon_package'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='sample_video_url',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]
