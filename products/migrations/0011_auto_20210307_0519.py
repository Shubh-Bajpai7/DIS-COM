# Generated by Django 3.1.6 on 2021-03-07 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20210305_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='name',
            name='name',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
