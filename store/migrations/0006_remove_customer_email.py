# Generated by Django 4.2.5 on 2023-09-15 05:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_alter_order_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='email',
        ),
    ]