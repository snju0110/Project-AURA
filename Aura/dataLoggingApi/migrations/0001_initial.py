# Generated by Django 4.0.8 on 2023-02-26 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='demDatatable',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=200)),
                ('amount', models.IntegerField()),
                ('sentFrom', models.CharField(max_length=200)),
                ('sentTo', models.CharField(max_length=200)),
                ('message', models.CharField(max_length=200)),
                ('primaryCat', models.CharField(max_length=200)),
                ('groupCat', models.CharField(max_length=200)),
            ],
        ),
    ]
