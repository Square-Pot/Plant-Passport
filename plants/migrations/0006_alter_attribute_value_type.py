# Generated by Django 3.2.4 on 2021-08-01 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0005_attribute_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='value_type',
            field=models.IntegerField(choices=[(1, 'String'), (2, 'Number')]),
        ),
    ]
