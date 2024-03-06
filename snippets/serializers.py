import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from phones.models import PhoneModel, Billings


# class PhoneSerializer(serializers.HyperlinkedModelSerializer):
#
#     image = serializers.ReadOnlyField(source='product.image')


# class PhoneModelForSerializer:
#     def __init__(self, phone_name, phone_cat_id):
#         self.phone_name = phone_name
#         self.phone_cat_id = phone_cat_id


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


# def encode():
#     model = PhoneModelForSerializer('Nokia123', 2)
#     model_sr = PhoneSerializer(model)
#     print(model_sr.data, type(model_sr), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
#
#
# def decode():
#     stream = io.BytesIO(b'{"phone_name":"Nokia123","phone_cat_id":2}')
#     data = JSONParser().parse(stream)
#     serializer = PhoneSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)


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
