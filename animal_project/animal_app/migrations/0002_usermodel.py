# Generated by Django 2.1.4 on 2018-12-26 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animal_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=10)),
                ('password', models.CharField(max_length=10)),
            ],
        ),
    ]
