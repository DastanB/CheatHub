# Generated by Django 2.1.2 on 2019-11-17 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20191117_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainuser',
            name='last_name',
            field=models.CharField(max_length=150),
        ),
    ]