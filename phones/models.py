from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.db import models
from ckeditor.fields import RichTextField


class Baskets(models.Model):
    basket_id = models.BigAutoField(primary_key=True)
    goods_name = models.CharField(max_length=50, blank=True, null=True)
    goods_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    goods_count = models.IntegerField(default=0)
    goods_id = models.IntegerField(blank=True, null=True)
    billing_id_id = models.IntegerField(default=0)

    def __str__(self):
        return self.goods_name

    class Meta:
        verbose_name = 'Елементи замовлення'
        verbose_name_plural = 'Елементи замовлення'
        db_table = 'baskets'


class Billings(models.Model):
    billing_id = models.BigAutoField(primary_key=True)
    status_phone = models.IntegerField(null=True, verbose_name='Статус Замовлення',
                                       choices=[(0, 'Не активне'), (1, 'Не оформленно'), (2, 'Оформленно'),
                                                (3, 'Оплачено'), (4, 'Відправленно у доставку'), (5, 'Доставлено')])
    full_price = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    billing_date = models.DateTimeField(auto_now_add=True, null=True,
                                        verbose_name='Дата створення замовлення')
    billing_update_date = models.DateTimeField(auto_now=True, null=True,
                                               verbose_name='Дата оновлення замовлення')
    billing_email = models.CharField(max_length=50, null=True, verbose_name='Email')
    billing_first_name = models.CharField(max_length=50, null=True, verbose_name="Ім'я")
    billing_second_name = models.CharField(max_length=50, null=True, verbose_name='Прізвище')
    billing_phone_number = models.CharField(max_length=15, null=True, verbose_name='Номер телефону')
    billing_address = models.CharField(max_length=100, null=True, verbose_name='Адреса Доставки')

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        db_table = 'billings'


class PhoneCategoryModel(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_name = models.CharField(max_length=50, verbose_name='Бренд', blank=True, null=True)
    cat_url = models.CharField(max_length=100, verbose_name='Посилання', blank=True, null=True)

    class Meta:
        db_table = 'phone_category'
        verbose_name = 'Категорії'
        verbose_name_plural = 'Категорії'


def category_fill():
    categories = PhoneCategoryModel.objects.all()
    cat_list = []
    for category in categories:
        cat_list.append((category.cat_id, category.cat_name))
    return cat_list


class PhoneModel(models.Model):
    phone_id = models.AutoField(primary_key=True)
    phone_cat_id = models.IntegerField(blank=True, null=True, choices=category_fill())
    phone_name = models.CharField(max_length=50, verbose_name='Назва')
    phone_description = RichTextField(blank=True, verbose_name='Опис')
    phone_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, verbose_name='Ціна')
    phone_image = models.ImageField(upload_to='phone_images/%Y/%mm/%d', null=True, blank=True,
                                    verbose_name='Головне Зображення')
    phone_additional_image_1 = models.ImageField(upload_to='phone_images/%Y/%mm/%d', null=True, blank=True,
                                                 verbose_name='Додаткове Зображення №1')
    phone_additional_image_2 = models.ImageField(upload_to='phone_images/%Y/%mm/%d', null=True, blank=True,
                                                 verbose_name='Додаткове Зображення №2')
    phone_additional_image_3 = models.ImageField(upload_to='phone_images/%Y/%mm/%d', null=True, blank=True,
                                                 verbose_name='Додаткове Зображення №3')

    phone_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата створення')
    phone_amount = models.IntegerField(null=True, verbose_name='Кількість на складі')

    def __str__(self):
        return self.phone_name

    def get_absolute_url(self):
        return reverse('view_phone', kwargs={'phone_id': self.pk})

    class Meta:
        verbose_name = 'Телефони'
        verbose_name_plural = 'Телефони'
        db_table = 'phones'
        ordering = ['phone_id']


class Pages(models.Model):
    page_id = models.AutoField(primary_key=True)
    page_name = models.CharField(max_length=50, verbose_name='Назва сторінки', blank=True, null=True)
    page_url = models.CharField(max_length=100, verbose_name='Посилання', blank=True, null=True)
    page_content = RichTextField(blank=True, verbose_name='Вміст сторінки')
    page_description = models.CharField(max_length=50, verbose_name='CEO', blank=True, null=True)
    page_status = models.BooleanField(default=True, verbose_name='Відображення сторінки')

    class Meta:
        verbose_name = 'Сторінки'
        verbose_name_plural = 'Сторінки'

