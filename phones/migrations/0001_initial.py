# Generated by Django 5.0.1 on 2024-01-20 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Baskets',
            fields=[
                ('basket_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('goods_name', models.CharField(blank=True, max_length=50, null=True)),
                ('goods_price', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
                ('goods_count', models.IntegerField(default=0)),
                ('goods_id', models.IntegerField(blank=True, null=True)),
                ('billing_id_id', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Елементи замовлення',
                'verbose_name_plural': 'Елементи замовлення',
                'db_table': 'baskets',
            },
        ),
        migrations.CreateModel(
            name='Billings',
            fields=[
                ('billing_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('status_phone', models.IntegerField(null=True)),
                ('full_price', models.DecimalField(decimal_places=0, max_digits=10, null=True)),
                ('billing_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата створення замовлення')),
                ('billing_update_date', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата оновлення замовлення')),
                ('billing_email', models.CharField(max_length=50, null=True, verbose_name='Email')),
                ('billing_first_name', models.CharField(max_length=50, null=True, verbose_name="Ім'я")),
                ('billing_second_name', models.CharField(max_length=50, null=True, verbose_name='Прізвище')),
                ('billing_phone_number', models.CharField(max_length=15, null=True, verbose_name='Номер телефону')),
                ('billing_address', models.CharField(max_length=100, null=True, verbose_name='Адреса Доставки')),
            ],
            options={
                'verbose_name': 'Замовлення',
                'verbose_name_plural': 'Замовлення',
                'db_table': 'billings',
            },
        ),
        migrations.CreateModel(
            name='PhoneModel',
            fields=[
                ('phone_id', models.AutoField(primary_key=True, serialize=False)),
                ('phone_name', models.CharField(max_length=50, verbose_name='Назва')),
                ('phone_description', models.TextField(blank=True, verbose_name='Опис')),
                ('phone_price', models.DecimalField(decimal_places=0, max_digits=10, null=True, verbose_name='Ціна')),
                ('phone_image', models.ImageField(upload_to='phone_images/%Y/%mm/%d', verbose_name='Зображення')),
                ('phone_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата створення')),
            ],
            options={
                'verbose_name': 'Телефони',
                'verbose_name_plural': 'Телефони',
                'db_table': 'phones',
                'ordering': ['phone_id'],
            },
        ),
    ]
