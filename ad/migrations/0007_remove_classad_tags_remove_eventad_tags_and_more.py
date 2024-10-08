# Generated by Django 5.0.7 on 2024-08-08 09:40

import taggit.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0006_rename_price_classad_fees_remove_classad_end_date_and_more'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classad',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='eventad',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='rentalad',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='salead',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='servicead',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='jobad',
            name='tags',
        ),
        migrations.AlterField(
            model_name='rentalad',
            name='period',
            field=models.CharField(choices=[('M', 'Month'), ('D', 'Day'), ('Y', 'Year')], default='D', max_length=1),
        ),
        migrations.AddField(
            model_name='jobad',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
