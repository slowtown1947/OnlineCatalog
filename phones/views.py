import logging
import pycurl
import certifi
from io import BytesIO

from rest_framework import generics
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django import template

from .forms import OrderForm, UserProfileForm
from .models import PhoneModel, Baskets, Billings, Pages, PhoneCategoryModel
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

logger = logging.getLogger('phones')

register = template.Library()


def get_curl(link):
    c = pycurl.Curl()
    c.setopt(c.URL, link)
    buffer = BytesIO()
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.CAINFO, certifi.where())
    c.perform()
    c.close()
    body = buffer.getvalue()
    return body.decode('utf-8')


def signup_user(request):
    """
    simple registration form
    email records as username
    template 'signup.html'
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['email'], password=request.POST['password1'],
                                                email=request.POST['email'], first_name=request.POST['first_name'],
                                                last_name=request.POST['last_name'])
                user.save()
                login(request, user)
                return redirect('homepage')
            except IntegrityError:
                return render(request, 'signup.html',
                              {'form': UserCreationForm(), 'error': "Це ім'я користувача вже використовується"})
        else:
            return render(request, 'signup.html', {'form': UserCreationForm(), 'error': 'Паролі не співпадають'})


def login_user(request):
    """
    simple login form
    template 'login.html'
    :param request:
    :return:
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, "Неправильне ім'я користувач або пароль.")
    return render(request, 'login.html')


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('homepage')


def user_profile_view(request):
    """
    render profile page where user can change profile info (
    first_name, last_name, email (username))
    :param request:
    :return:
    """
    template_name = 'profile.html'

    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.username = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'Зміни збережено успішно.')
            return redirect('homepage')
    else:
        form = UserProfileForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })

    return render(request, template_name, {'form': form})


def history_view(request):
    phone_objects = PhoneModel.objects.all()
    tmp_view_history = request.session.get('view_history')
    view_history = []
    if tmp_view_history == [] or tmp_view_history is None:
        pass
    else:
        for history_object in tmp_view_history:
            for phone_obj in phone_objects:
                if int(phone_obj.phone_id) == int(history_object):
                    view_history.append(phone_obj)
    return view_history


def main_page(request):
    return redirect('homepage')


def catalog_paginator(request, general_array):
    page = request.GET.get('page')
    if page is None:
        page = 1
    per_page = 6
    paginator = Paginator(general_array, per_page)
    return paginator.page(page)


def home_manager(request, phone_objects, tmp_session):
    tmp_array = []
    out_of_stock_list = []
    for my_phone in phone_objects:
        tmp_buy_button_disabled = ''  # it's buy button disable trigger
        tmp_good_disabler = ''

        for session_phone in tmp_session:
            if str(session_phone[0]) == str(my_phone.phone_id):
                tmp_buy_button_disabled = 'disabled'

        if tmp_buy_button_disabled == 'disabled':
            if my_phone.phone_amount == 0:
                tmp_good_disabler = 'disabled'
                out_of_stock_list.append([my_phone, 'disabled', tmp_good_disabler])
            else:
                tmp_array.append([my_phone, 'disabled', ''])
        else:
            if my_phone.phone_amount == 0:
                tmp_good_disabler = 'disabled'
                out_of_stock_list.append([my_phone, '', tmp_good_disabler])
            else:
                tmp_array.append([my_phone, '', ''])
    tmp_array += out_of_stock_list
    return tmp_array


def homepage(request):
    """
    homepage view | creates session if not created yet
    create simple paginator
    render 2 objects:
    session_phones (list of all elements (phones) in session,
    general_array (paginator object that also contains data from phones table
    and trigger for purchase button)
    :param request:
    :return:
    """

    tmp_phone_objects = get_curl('http://127.0.0.1:8000/api/v1/testlist/')

    print(tmp_phone_objects)

    phone_objects = PhoneModel.objects.all()

    if request.session.get('picked_item') is not None:
        pass
    else:
        request.session['picked_item'] = []
    tmp_session = request.session.get('picked_item')

    general_array = home_manager(request, phone_objects, tmp_session)

    phones_paginator = catalog_paginator(request, general_array)

    view_history = history_view(request)

    context = {
        'session_phones': request.session.get('picked_item'),
        'general_array': phones_paginator,
        'view_history': view_history}
    return render(request, 'home.html', context)


def phone_category_brand(request, cat):
    cat_obj = PhoneCategoryModel.objects.get(cat_url=cat)
    phone_objects = PhoneModel.objects.filter(phone_cat_id=cat_obj.cat_id)
    tmp_session = request.session.get('picked_item')

    phone_objects = home_manager(request, phone_objects, tmp_session)

    phones_paginator = catalog_paginator(request, phone_objects)

    view_history = history_view(request)
    return render(request, 'phone_categories.html', {'general_array': phones_paginator, 'view_history': view_history})


def view_phone(request, phone_id):
    """
    render page of specific item by phone_id
    with trigger for purchase button
    create view history in session
    :param request:
    :param phone_id:
    :return:
    """
    phone_post = get_object_or_404(PhoneModel, pk=phone_id)
    phone_id_item = str(phone_post.phone_id)
    tmp_session = request.session.get('picked_item')
    buy_button_trigger = ''

    for item_in_session in tmp_session:
        if item_in_session[0] == phone_id_item:
            buy_button_trigger = 'disabled'
    if request.session.get('view_history') == [] or request.session.get('view_history') is None:
        request.session['view_history'] = [phone_id]
    elif len(request.session.get('view_history')) <= 4:
        if phone_id in request.session.get('view_history'):
            pass
        else:
            tmp_view_history = request.session.get('view_history')
            tmp_view_history.append(phone_id)
            request.session['view_history'] = tmp_view_history

    else:
        if phone_id not in request.session.get('view_history'):
            request.session['view_history'] = request.session.get('view_history')[1:]
            request.session['view_history'].append(phone_id)
    view_history = history_view(request)
    if phone_post.phone_amount == 0:
        out_of_stock_disabler = 'disabled'
    else:
        out_of_stock_disabler = ''
    if request.method == 'GET':
        return render(request, 'view_phone.html', {'phone_post': phone_post, 'buy_button_trigger': buy_button_trigger,
                                                   'out_of_stock_disabler': out_of_stock_disabler,
                                                   'view_history': view_history})


def cart(request):
    """
    append detail of picked phone item to session if it doesn't exist already
    and make redirect with data to get_cart() function
    elements of request.session.get('picked_item') contains:
    id, name, price, date, count, trigger for plus/minus button
    change trigger to active (cart_item[5] = 'disabled') in case if
    there is only 1 item in table phones left
    :param request:
    :return:
    """
    request.session.get('picked_item')

    goods_in_cart = request.session.get('picked_item')
    print(type(request.session.get('picked_item')))
    if goods_in_cart is None:
        goods_in_cart = [str(request.POST.get('id')), request.POST.get('name'),
                         request.POST.get('price'), request.POST.get('date'), 1, '']
    elif goods_in_cart == "":
        goods_in_cart = [[str(request.POST.get('id')), request.POST.get('name'),
                          request.POST.get('price'), request.POST.get('date'), 1, '']]
    else:
        tmp_item = ([str(request.POST.get('id')), request.POST.get('name'),
                     request.POST.get('price'), request.POST.get('date'), 1, ''])

        if tmp_item in goods_in_cart:
            pass
        else:
            goods_in_cart.append([str(request.POST.get('id')), request.POST.get('name'),
                                  request.POST.get('price'), request.POST.get('date'), 1, ''])
    request.session['picked_item'] = goods_in_cart
    tmp_session_cart = request.session.get('picked_item')
    for cart_item in tmp_session_cart:
        phone_object = PhoneModel.objects.get(phone_id=str(cart_item[0]))
        if phone_object.phone_amount == 1:
            cart_item[5] = 'disabled'
    request.session['picked_item'] = tmp_session_cart

    print(request.session.get('picked_item'))

    return redirect('/get_cart')


def get_cart(request):
    """
    render cart page with data from session (request.session.get('picked_item'))
    renders 3 objects in context:
    goods_in_cart (items of cart), total_cost (total price of elements in cart),
    cart_disabler (trigger for to order button)
    :param request:
    :return:
    """
    total_cost = 0
    # CLEAN SESSION IN CASE IF NEEDED
    # request.session['picked_item'] = ''
    if request.session.get('picked_item') == [] or request.session.get('picked_item') == "" \
            or request.session.get('picked_item') == None:
        cart_disabler = ''
    else:
        for item in request.session.get('picked_item'):
            total_cost += int(item[2]) * item[4]
        if total_cost == 0:
            cart_disabler = 'disabled'
        else:
            cart_disabler = ''
    print(request.session.get('picked_item'))
    return render(request, 'cart.html', {'goods_in_cart': request.session.get('picked_item'), 'total_cost': total_cost,
                                         'cart_disabler': cart_disabler})


def delete_item_in_cart(request):
    """
    button to delite specific item from cart by id and redirect to get_cart view
    :param request:
    :return:
    """
    tmp_session_del = request.session.get('picked_item')
    for cart_item in tmp_session_del:
        if str(cart_item[0]) == request.POST.get('id'):
            delete_index = tmp_session_del.index(cart_item)
            del tmp_session_del[delete_index]
            request.session['picked_item'] = tmp_session_del

    return redirect('get_cart')


def plus_button_in_cart(request):
    """
    button to increase amount in cart of specific item
    add trigger (cart_item[5] = 'disabled') for disabling plus button
    in case if there is no more items in table phones
    :param request:
    :return:
    """
    tmp_session_plus = request.session.get('picked_item')
    print(tmp_session_plus)
    for cart_item in tmp_session_plus:
        if str(cart_item[0]) == request.POST.get('id'):
            phone_object = PhoneModel.objects.get(phone_id=str(cart_item[0]))
            if cart_item[4] < phone_object.phone_amount:
                cart_item[4] = cart_item[4] + 1
                if cart_item[4] == phone_object.phone_amount:
                    cart_item[5] = 'disabled'

            else:
                request.session['add_button_disabler'] = 'disabled'
                cart_item[5] = 'disabled'

            request.session['picked_item'] = tmp_session_plus
    return redirect('get_cart')


def minus_button_in_cart(request):
    """
    button to reduce amount in cart of specific item
    delete trigger (cart_item[5] = '') for disabling plus button
    in case if there is still items in table phones
    :param request:
    :return:
    """
    tmp_session_minus = request.session.get('picked_item')
    for cart_item in tmp_session_minus:
        if str(cart_item[0]) == request.POST.get('id'):
            print(request.session.get('picked_item'))
            cart_item[4] = cart_item[4] - 1
            request.session['picked_item'] = tmp_session_minus

            if cart_item[4] == 0:
                delete_item_in_cart(request)
            elif cart_item[5] == 'disabled':
                cart_item[5] = ''
                return redirect('get_cart')
            elif cart_item[5] == '':
                return redirect('get_cart')

    return redirect('get_cart')


def clear_cart(request):
    """
    clear all cart session
    :param request:
    :return:
    """
    request.session['picked_item'] = []
    return redirect('get_cart')


def finish_order(request):
    """
    takes all items from cart (session),
    create billings and baskets objects and fill them with data from cart,
    send billing_id to session (request.session['billing_item'] = billing.billing_id),
    clear all cart (session) and redirect 'to_order'
    :param request:
    :return:
    """
    tmp_session_order = request.session['picked_item']
    if tmp_session_order == []:
        return redirect('get_cart')
    else:
        full_price_of_order = 0
        if request.method == "POST":
            for billing_item in tmp_session_order:  # here creates and save billing
                full_price_of_order += int(billing_item[2]) * billing_item[4]
            billing = Billings(status_phone=1, full_price=full_price_of_order)  # status_phone=1 - active
            billing.save()

            for basket_item in tmp_session_order:  # here creates and save basket
                # example: basket_item ['4', 'Xiaomi 13T Pro', '640', '20 грудня 2023 р. 12:46', 1]
                phone_name = basket_item[1]
                phone_price = basket_item[2]
                phone_id = basket_item[0]
                billing_id = billing.billing_id
                count_of_items = basket_item[4]
                basket = Baskets(goods_name=phone_name, goods_price=phone_price, goods_id=phone_id,
                                 billing_id_id=billing_id, goods_count=count_of_items)
                basket.save()
                request.session['billing_item'] = billing.billing_id
            clear_cart(request)
            billing_log = f'def finish_order CREATED new billing: {billing.billing_id}'
            logger.info(billing_log)
            return redirect('to_order')


def to_order(request):  # send items from cart to "to_order" page
    """
    render 'to_order.html' this page for using finalising order
    and fills the form with already existing information
    if user is not authenticated redirects to confirm_order_non_register_user view
    context: ordering_items (cart items), final_price (total cart price),
    bill_id (billing_id), form
    :param request:
    :return:
    """

    bill_id = request.session.get('billing_item')
    ordering_items = []
    final_price = 0
    cart_objects = Baskets.objects.all()
    for cart_object in cart_objects:
        if cart_object.billing_id_id == bill_id:
            items_price = int(cart_object.goods_price * cart_object.goods_count)
            final_price += items_price
            ordering_items.append([cart_object, items_price])
    if request.user.is_authenticated:
        form = OrderForm(request.POST)
        if form.is_valid():
            request.session['form_detail'] = form.cleaned_data
            return redirect(confirm_order_non_register_user, bill_id=bill_id)
    else:
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                request.session['form_detail'] = form.cleaned_data
                return redirect(confirm_order_non_register_user, bill_id=bill_id)
        else:
            form = OrderForm()
    return render(request, 'to_order.html',
                  {'ordering_items': ordering_items, 'final_price': final_price, 'bill_id': bill_id, 'form': form})


def confirm_order_non_register_user(request, bill_id):
    """
    fills the order with relevant information

    :param bill_id:,
    :param request:
    :return:
    """
    tmp_detail_session = request.session['form_detail']
    Billings.objects.filter(billing_id=bill_id).update(billing_email=tmp_detail_session['email'],
                                                       billing_first_name=tmp_detail_session['first_name'],
                                                       billing_second_name=tmp_detail_session['last_name'],
                                                       billing_phone_number=tmp_detail_session['phone'],
                                                       billing_address=tmp_detail_session['address'],
                                                       status_phone=2)
    if request.user.is_authenticated:
        return render(request, 'order_done.html', {'bill_id': bill_id})
    else:
        return render(request, 'order_done.html', {'bill_id': bill_id})


def edit_page(request):
    """
    render page with already created orders
    page has is_staff restriction
    each order can be opened with view_billing view
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        username = request.user.username
    else:
        print('User is not auth')
        return render(request, 'home.html')
    user = User.objects.get(username=username)
    if user.is_staff == 1:
        is_staff = "True"
        print(is_staff)
        billings_array = Billings.objects.all()
        print(billings_array)
        return render(request, 'edit_page.html', {'is_staff': is_staff, 'billings_array': billings_array})
    else:
        is_staff = "False"
        print(is_staff)
    return render(request, 'edit_page.html', {'is_staff': is_staff})


def view_billing(request, billing_id):
    """
    UNFINISHED
    page for view contents of existing orders
    :param request:
    :param billing_id:
    :return:
    """
    full_basket = Baskets.objects.all()
    basket_array = []
    basket_num = 1
    for basket_item in full_basket:
        if basket_item.billing_id_id == billing_id:
            phone = PhoneModel.objects.get(phone_id=basket_item.goods_id)
            billing = Billings.objects.get(billing_id=billing_id)
            basket_array.append([basket_item, basket_num, phone.phone_image, billing.full_price])
            print(basket_array)
            basket_num += 1
    test_var = f'def view_billing entering bill_id: {billing_id}'
    logger.info(test_var)
    return render(request, 'view_billing.html', {'basket_array': basket_array, 'billing_id': billing_id})


def page_generator(request, page_url):
    print(page_url)
    page_object = Pages.objects.get(page_url=page_url)
    return render(request, 'page_blanket.html', {'page': page_object})


def test_view(request):
    return HttpResponse('hi')
