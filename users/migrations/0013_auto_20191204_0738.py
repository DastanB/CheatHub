# Generated by Django 2.1.2 on 2019-12-04 07:38

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20191203_1844'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='activation',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='mainuser',
            name='full_name',
            field=models.CharField(blank=True, max_length=181),
        ),
    ]
