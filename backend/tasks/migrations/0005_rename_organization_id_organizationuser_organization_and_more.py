# Generated by Django 4.2.2 on 2023-07-03 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_alter_organizationuser_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organizationuser',
            old_name='organization_id',
            new_name='organization',
        ),
        migrations.RenameField(
            model_name='organizationuser',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='projectuser',
            old_name='project_id',
            new_name='project',
        ),
        migrations.RenameField(
            model_name='projectuser',
            old_name='user_id',
            new_name='user',
        ),
    ]
