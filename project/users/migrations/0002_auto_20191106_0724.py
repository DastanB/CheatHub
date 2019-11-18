# Generated by Django 2.1.2 on 2019-11-06 07:24

from django.db import migrations, models
import django.db.models.deletion
import utils.upload
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterModelManagers(
            name='mainuser',
            managers=[
            ],
        ),
        migrations.RenameField(
            model_name='mainuser',
            old_name='is_creator',
            new_name='is_customer',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='address',
        ),
        migrations.AlterField(
            model_name='mainuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='mainuser',
            name='first_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='mainuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.FileField(upload_to=utils.upload.avatar_path, validators=[utils.validators.validate_file_size, utils.validators.validate_extension]),
        ),
        migrations.AddField(
            model_name='profile',
            name='university',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.University'),
        ),
    ]
