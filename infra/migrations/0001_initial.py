# Generated by Django 4.0.5 on 2022-07-05 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('currentBlockHeight', models.IntegerField()),
                ('healthy', models.BooleanField()),
            ],
        ),
    ]