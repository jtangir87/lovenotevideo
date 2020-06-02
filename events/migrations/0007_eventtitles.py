# Generated by Django 2.2.10 on 2020-06-02 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20200531_2216'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventTitles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Start Title')),
                ('end_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='End Title')),
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='titles', to='events.Event')),
            ],
        ),
    ]
