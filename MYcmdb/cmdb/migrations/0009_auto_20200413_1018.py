# Generated by Django 2.1.5 on 2020-04-13 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0008_variable2group_variable2server'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asset',
            name='node',
        ),
        migrations.RemoveField(
            model_name='asset',
            name='tag',
        ),
    ]