# Generated by Django 2.2.10 on 2021-02-10 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_timezone'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='referral',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
