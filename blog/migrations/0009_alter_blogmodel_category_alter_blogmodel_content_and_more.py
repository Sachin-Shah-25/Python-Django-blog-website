# Generated by Django 5.2.4 on 2025-07-17 14:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_remove_blogmodel_likes_alter_blogmodel_dateandtime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogmodel',
            name='category',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='blogmodel',
            name='content',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='blogmodel',
            name='dateandtime',
            field=models.DateTimeField(default=datetime.datetime(2025, 7, 17, 20, 2, 13, 443677)),
        ),
        migrations.AlterField(
            model_name='commentmodel',
            name='comment',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='commentmodel',
            name='dateandtime',
            field=models.DateTimeField(default=datetime.datetime(2025, 7, 17, 20, 2, 13, 444677)),
        ),
    ]
