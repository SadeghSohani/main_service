# Generated by Django 4.0.3 on 2022-04-14 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flights',
            name='reserved',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
