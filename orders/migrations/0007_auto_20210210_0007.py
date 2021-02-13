# Generated by Django 2.2.10 on 2021-02-10 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_package_sample_video_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='approved_videos',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='package',
            name='editor_min_pay',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='package',
            name='editor_per_video_pay',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4),
        ),
    ]
