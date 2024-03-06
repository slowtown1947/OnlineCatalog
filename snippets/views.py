from django.forms import model_to_dict
from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from phones.models import PhoneModel, Billings, Baskets

from snippets.serializers import PhoneSerializer, BillingSerializer, PhoneForTgBotSerializer, BillingGETOnlySerializer


class PhoneListAPIView(APIView):

    def get(self, request):
        w = PhoneModel.objects.all().exclude(phone_amount=0)  # send only in stock items
        return Response({'objects': PhoneForTgBotSerializer(w, many=True).data})  # many=True is important

    def post(self, request):
        post_new = PhoneModel.objects.create(phone_name=request.data['phone_name'],
                                             phone_cat_id=request.data['phone_cat_id'],
                                             phone_price=request.data['phone_price'],
                                             phone_image=request.data['phone_image'])

        return Response({'post': PhoneSerializer(post_new).data})


class BillingObjectAPIView(APIView):

    def get(self, request, billing_phone_number):
        lst = Billings.objects.filter(billing_phone_number=billing_phone_number)

        serializer = BillingGETOnlySerializer(lst, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# post simple billing and all basket objects in one post request
class BillingAPIView(APIView):

    def get(self, request):
        lst = Billings.objects.all()
        serializer = BillingSerializer(lst, many=True)

        return Response({'objects': serializer.data})

    def post(self, request):
        post_new_billing = Billings.objects.create(status_phone=int(request.data['status_phone']),
                                                   full_price=request.data['full_price'],
                                                   billing_email=request.data['billing_email'],
                                                   billing_first_name=request.data['billing_first_name'],
                                                   billing_second_name=request.data['billing_second_name'],
                                                   billing_phone_number=request.data['billing_phone_number'],
                                                   billing_address=request.data['billing_address'])

        dict_baskets = eval(request.data['goods_id_dict'])
        for obj_id, obj_count in dict_baskets.items():
            tmp_obj = PhoneModel.objects.get(phone_id=obj_id)
            print(tmp_obj.phone_name)
            post_new_basket = Baskets.objects.create(goods_name=tmp_obj.phone_name,
                                                     goods_price=tmp_obj.phone_price,
                                                     goods_count=obj_count,
                                                     goods_id=obj_id,
                                                     billing_id_id=post_new_billing.billing_id)
            Response({'post': model_to_dict(post_new_basket)})

        return Response({'post': model_to_dict(post_new_billing)})
