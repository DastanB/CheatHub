# Generated by Django 2.1.2 on 2019-11-18 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20191118_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainuser',
            name='username',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
