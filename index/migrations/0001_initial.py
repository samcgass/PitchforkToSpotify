# Generated by Django 3.0.6 on 2020-05-07 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tokens',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.SlugField(max_length=255)),
                ('refresh_token', models.SlugField(max_length=255)),
            ],
        ),
    ]
