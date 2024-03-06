
from rest_framework import serializers
from phones.models import Billings


class PhoneSerializer(serializers.Serializer):
    phone_id = serializers.IntegerField()
    phone_cat_id = serializers.IntegerField()
    phone_name = serializers.CharField(max_length=50)
    phone_description = serializers.CharField()
    phone_price = serializers.DecimalField(max_digits=10, decimal_places=0)
    phone_image = serializers.ImageField(allow_empty_file=True)
    phone_additional_image_1 = serializers.ImageField(allow_empty_file=True)
    phone_additional_image_2 = serializers.ImageField(allow_empty_file=True)
    phone_additional_image_3 = serializers.ImageField(allow_empty_file=True)
    phone_date = serializers.DateTimeField()
    phone_amount = serializers.IntegerField()


class PhoneForTgBotSerializer(serializers.Serializer):
    phone_id = serializers.IntegerField()
    phone_cat_id = serializers.IntegerField()
    phone_name = serializers.CharField(max_length=50)
    phone_price = serializers.DecimalField(max_digits=10, decimal_places=0)
    phone_image = serializers.ImageField(allow_empty_file=True)
    phone_date = serializers.DateTimeField()
    phone_amount = serializers.IntegerField()


class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billings
        fields = ('status_phone', 'full_price', 'billing_email', 'billing_first_name', 'billing_second_name',
                  'billing_phone_number', 'billing_address', 'goods_id_dict',)


class BillingGETOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Billings
        fields = (
            'billing_id', 'status_phone', 'full_price', 'billing_date', 'billing_email', 'billing_first_name',
            'billing_second_name', 'billing_phone_number', 'billing_address')

# class BasketsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Billings
#         fields = ('goods_id_dict',)
