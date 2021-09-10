# Generated by Django 3.0.6 on 2021-09-10 03:32

import SmartDjango.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0005_auto_20180927_1035'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'default_manager_name': 'objects'},
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=SmartDjango.models.fields.CharField(blank=True, default=None, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='description',
            field=SmartDjango.models.fields.CharField(blank=True, default=None, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=SmartDjango.models.fields.CharField(blank=True, default=None, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='port',
            field=SmartDjango.models.fields.PositiveSmallIntegerField(default=0, unique=True, verbose_name='SS端口'),
        ),
        migrations.AlterField(
            model_name='user',
            name='qt_user_app_id',
            field=SmartDjango.models.fields.CharField(default=None, max_length=16),
        ),
        migrations.AlterField(
            model_name='user',
            name='qtb_token',
            field=SmartDjango.models.fields.CharField(default=None, max_length=256),
        ),
        migrations.AlterField(
            model_name='user',
            name='ss_change_time',
            field=SmartDjango.models.fields.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='ss_pwd',
            field=SmartDjango.models.fields.CharField(default=None, max_length=32, verbose_name='SS密码'),
        ),
    ]