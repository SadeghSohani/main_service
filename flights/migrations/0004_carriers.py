# Generated by Django 4.0.3 on 2022-04-16 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0003_planes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carriers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=200)),
                ('raiting', models.IntegerField()),
            ],
        ),
    ]