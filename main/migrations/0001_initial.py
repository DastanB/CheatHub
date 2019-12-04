# Generated by Django 2.1.2 on 2019-12-03 18:44

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils.upload
import utils.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=10000000)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='CommentReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=10000000)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=10000)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('due_to', models.DateTimeField()),
                ('price', models.PositiveIntegerField()),
                ('payment_type', models.PositiveSmallIntegerField(choices=[(1, 'By card'), (2, 'By cash')], default=2)),
                ('order_type', models.PositiveSmallIntegerField(choices=[(1, 'Essay'), (2, 'Math problems'), (3, 'IT project')], null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_orders', to=settings.AUTH_USER_MODEL)),
                ('executor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='todo_tasks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to=utils.upload.order_document_path, validators=[utils.validators.validate_file_size, utils.validators.validate_extension])),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='main.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField()),
                ('reciever', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews_to_me', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='commentreview',
            name='review',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.Review'),
        ),
        migrations.AddField(
            model_name='commentreview',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_comment_to_reviews', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commentorder',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='main.Order'),
        ),
        migrations.AddField(
            model_name='commentorder',
            name='reciever',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments_to_me', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commentorder',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_comments', to=settings.AUTH_USER_MODEL),
        ),
    ]
