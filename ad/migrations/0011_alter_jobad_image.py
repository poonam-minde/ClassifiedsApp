# Generated by Django 5.0.7 on 2024-08-22 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0010_remove_eventmessage_ad_remove_eventmessage_parent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobad',
            name='image',
            field=models.ImageField(blank=True, default='static/img/default_job.jpg', null=True, upload_to='images/jobs'),
        ),
    ]
