# Generated by Django 3.0.4 on 2020-06-06 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    operations = [
        migrations.CreateModel(
            name='WorkersInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('worker_id', models.TextField()),
                ('free_comments', models.TextField()),
            ],
        ),
    ]
