# Generated by Django 4.2.2 on 2023-07-06 06:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0007_alter_organizationuser_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_organizations', to=settings.AUTH_USER_MODEL),
        ),
    ]
