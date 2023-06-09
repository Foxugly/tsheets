# Generated by Django 4.2 on 2023-05-23 13:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('days', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projectcategories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('lock', models.BooleanField(default=False)),
                ('refer_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='back_slot_projectcategory', to='projectcategories.projectcategory', verbose_name='category')),
                ('refer_day', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='back_slot_day', to='days.day', verbose_name='Day')),
                ('refer_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='back_slot_user', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'slot',
                'verbose_name_plural': 'slots',
                'ordering': ('pk',),
            },
        ),
    ]
