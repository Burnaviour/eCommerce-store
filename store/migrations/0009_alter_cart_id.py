# Generated by Django 4.2.5 on 2023-09-13 07:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
