# Generated by Django 4.1.2 on 2024-06-30 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200706_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='testfilepath',
            name='is_user_upload',
            field=models.BooleanField(default=False),
        ),
    ]