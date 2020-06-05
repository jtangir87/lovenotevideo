# Generated by Django 2.2.10 on 2020-06-03 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_eventtitles'),
        ('django_simple_coupons', '0001_initial'),
        ('orders', '0002_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventCoupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_value', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='django_simple_coupons.Coupon')),
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='coupon', to='events.Event')),
            ],
        ),
    ]