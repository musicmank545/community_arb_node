# Generated by Django 4.0.5 on 2022-07-05 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infra', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='address',
            field=models.CharField(default='127.0.0.1', max_length=250),
            preserve_default=False,
        ),
    ]
