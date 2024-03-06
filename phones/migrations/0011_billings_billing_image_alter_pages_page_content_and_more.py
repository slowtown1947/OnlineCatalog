# Generated by Django 5.0.1 on 2024-02-15 19:21

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phones', '0010_phonecategorymodel_alter_pages_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='billings',
            name='billing_image',
            field=models.ImageField(blank=True, null=True, upload_to='billing_image/%Y/%mm/%d'),
        ),
        migrations.AlterField(
            model_name='pages',
            name='page_content',
            field=ckeditor.fields.RichTextField(blank=True, verbose_name='Вміст сторінки'),
        ),
        migrations.AlterField(
            model_name='phonemodel',
            name='phone_cat_id',
            field=models.IntegerField(blank=True, choices=[(1, 'Apple'), (2, 'Xiaomi'), (3, 'Samsung'), (4, 'Google'), (5, 'Motorola'), (6, 'Realme')], null=True),
        ),
    ]
