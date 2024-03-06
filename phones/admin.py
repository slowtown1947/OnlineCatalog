from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import PhoneModel, Baskets, Billings, Pages, PhoneCategoryModel


class PhoneAdmin(admin.ModelAdmin):
    list_display = ('phone_id', 'phone_name', 'phone_price', 'phone_amount', 'phone_image', 'phone_date')
    list_display_links = ('phone_id', 'phone_name')
    search_fields = ('phone_name', 'phone_description')
    readonly_fields = ["phone_image_main", "phone_image_add_1", "phone_image_add_2", "phone_image_add_3"]

    def phone_image_main(self, obj):
        return mark_safe('<img src="{url}" height={height} />'.format(
            url=obj.phone_image.url,
            height=250, ))

    def phone_image_add_1(self, obj):
        return mark_safe('<img src="{url}" height={height} />'.format(
            url=obj.phone_additional_image_1.url,
            height=250, ))

    def phone_image_add_2(self, obj):
        return mark_safe('<img src="{url}" height={height} />'.format(
            url=obj.phone_additional_image_2.url,
            height=250, ))

    def phone_image_add_3(self, obj):
        return mark_safe('<img src="{url}" height={height} />'.format(
            url=obj.phone_additional_image_3.url,
            height=250, ))


class BasketAdmin(admin.ModelAdmin):
    list_display = ('basket_id', 'billing_id_id', 'goods_name', 'goods_price', 'goods_count', 'goods_id')
    list_display_links = ('basket_id', 'goods_name')
    search_fields = ('billing_id_id', 'goods_id')


class BillingAdmin(admin.ModelAdmin):
    list_display = ('billing_id', 'status_phone', 'full_price', 'billing_date', 'billing_update_date', 'billing_email',
                    'billing_first_name', 'billing_second_name', 'billing_phone_number', 'billing_address')
    list_display_links = ('billing_id', 'status_phone', 'billing_date')
    search_fields = ('billing_id', 'status_phone', 'billing_email')


class PagesAdmin(admin.ModelAdmin):
    list_display = ('page_id', 'page_name', 'page_url', 'page_status')
    list_display_links = ('page_id', 'page_name', 'page_url')


class PhoneCategoryModelAdmin(admin.ModelAdmin):
    list_display = ('cat_id', 'cat_name', 'cat_url')
    list_display_links = ('cat_id', 'cat_name', 'cat_url')


admin.site.register(PhoneCategoryModel, PhoneCategoryModelAdmin)
admin.site.register(Pages, PagesAdmin)
admin.site.register(PhoneModel, PhoneAdmin)
admin.site.register(Baskets, BasketAdmin)
admin.site.register(Billings, BillingAdmin)

# class MyAdmin(admin.ModelAdmin):
#     def has_change_permission(self, request, obj=None):
#         return True
