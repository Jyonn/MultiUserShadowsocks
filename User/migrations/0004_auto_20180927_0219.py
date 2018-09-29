# Generated by Django 2.0 on 2018-09-27 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_auto_20180222_2254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='grant',
        ),
        migrations.RemoveField(
            model_name='user',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='user',
            name='password',
        ),
        migrations.RemoveField(
            model_name='user',
            name='pwd_change_time',
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.CharField(blank=True, default=None, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='qt_user_app_id',
            field=models.CharField(default=None, max_length=16),
        ),
        migrations.AddField(
            model_name='user',
            name='qtb_token',
            field=models.CharField(default=None, max_length=256),
        ),
    ]