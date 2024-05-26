import telebot
from telebot import types
import pycurl
import certifi
from io import BytesIO
import webbrowser
import json

bot = telebot.TeleBot("#")

main_link = 'http://slowtown.pythonanywhere.com/'

cart_dict_id = {}  # {phone_id: phone_amount}
parsed_data = {}  # data for post request
user_input = {}  # don't touch it


# get curl method
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


# post curl method
def post_curl(data, link):
    url = link
    # headers = {'Content-Type': 'application/json'}
    c = pycurl.Curl()
    c.setopt(pycurl.URL, '%s' % url)
    c.setopt(pycurl.HTTPHEADER, ['Accept: application/json', 'Content-Type: application/json'])
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.POSTFIELDS, data)
    c.perform()


# callback for buttons
@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call):
    if call.data == 'go_to_site':
        webbrowser.open(main_link)
    elif call.data == 'order_details':
        bot.send_message(call.message.chat.id, 'Enter your phone number:')
        bot.register_next_step_handler(call.message, order_by_number_callback)
    elif call.data == 'create_order':
        create_order_callback(call.message.chat.id)
    elif call.data == 'add_goods_to_cart':
        bot.send_message(call.message.chat.id,
                         "If you want to select a product - enter the name\n(for example: Apple iPhone 15 Pro Max)")
        bot.register_next_step_handler(call.message, add_goods_to_cart)
    elif call.data == 'remove_goods_from_cart':
        bot.send_message(call.message.chat.id,
                         "If you want to remove a product from the cart - enter the name\n"
                         "(for example: Apple iPhone 15 Pro Max)")
        bot.register_next_step_handler(call.message, remove_goods_from_cart)
    elif call.data == 'remove_order':
        remove_order(call.message.chat.id)
    elif call.data == 'remove_order_yes':
        remove_order_yes(call.message.chat.id)
    elif call.data == 'remove_order_no':
        remove_order_no(call.message.chat.id)
    elif call.data == 'review_shopping_list':
        review_shopping_list(call.message.chat.id)
    elif call.data == 'finish_cart':
        finish_cart(call.message)
    elif call.data == 'cancel_order':
        cancel_order(call.message.chat.id)
    elif call.data == 'confirm_order':
        confirm_order(call.message.chat.id)


# start button func
@bot.message_handler(commands=['start'])
def main(message):
    markup = types.InlineKeyboardMarkup()
    btn_order_check = types.InlineKeyboardButton('Check order details', callback_data='order_details')
    # btn_site = types.InlineKeyboardButton('Go to site', callback_data='go_to_site')
    btn_order_create = types.InlineKeyboardButton('Place an order', callback_data='create_order')
    # markup.add(btn_site)
    markup.add(btn_order_check)
    markup.add(btn_order_create)
    bot.send_message(message.chat.id,
                     f'Hello, {message.from_user.first_name}\n'
                     f'Here you can check the details of your order or place a new one.', reply_markup=markup)


# get order info with phone number by post request
def order_by_number_callback(message):
    status_dict = {0: 'Inactive', 1: 'Not processed', 2: 'Processed',
                   3: 'Paid', 4: 'Sent for delivery', 5: 'Delivered'}
    bill_info = get_curl(f'{main_link}api/v1/testbill/{message.text}')
    info_json = json.loads(bill_info)
    print(info_json)
    response = "Your order(s):\n\n"
    for order_info in info_json:
        response += f"Order number: {order_info['billing_id']}\nOrder cost: {order_info['full_price']}" \
                   f"\nOrder status: {status_dict.get(order_info['status_phone'])}\n\n"
    bot.send_message(message.chat.id, response)
    main(message)


# method for getting with post request and parsing data about all goods
def get_goods_utility():
    json_data = get_curl(f'{main_link}api/v1/testlist/')
    parsed_data_goods = json.loads(json_data)
    price_list = "Our assortment:\n\n"

    for phone in parsed_data_goods["objects"]:
        price_list += f"{phone['phone_name']}, Price: {phone['phone_price']} euros, Quantity: {phone['phone_amount']}\n"

    return [price_list, parsed_data_goods]


def cart_info_utility():
    cart_sum = 0
    order_str = "Your order: \n"

    for id, amount in cart_dict_id.items():
        for goods in goods_info_json["objects"]:
            if id == goods["phone_id"]:
                order_str += f'{goods["phone_name"]} {amount} pcs\n'
                cart_sum += int(goods["phone_price"]) * int(amount)

    order_str += f"Order total: {cart_sum} euros."
    return [order_str, cart_sum]


def create_order_callback(message):
    goods_str = get_goods_utility()[0]
    # print(goods_info_json["objects"])
    markup = types.InlineKeyboardMarkup()
    btn_add_goods = types.InlineKeyboardButton('Add product', callback_data='add_goods_to_cart')
    btn_remove_goods = types.InlineKeyboardButton('Remove product', callback_data='remove_goods_from_cart')
    btn_remove_oder = types.InlineKeyboardButton('Cancel order', callback_data='remove_order')
    btn_finish_cart = types.InlineKeyboardButton('Place order', callback_data='finish_cart')
    btn_review = types.InlineKeyboardButton('View products', callback_data='review_shopping_list')
    # print(cart_dict_id)

    if cart_dict_id == {}:
        markup.add(btn_add_goods, btn_remove_goods)
        bot.send_message(message, goods_str, reply_markup=markup)
    else:
        markup.add(btn_add_goods, btn_remove_goods)
        markup.add(btn_remove_oder)
        markup.add(btn_finish_cart)
        markup.add(btn_review)

        order_str = cart_info_utility()[0]

        bot.send_message(message, order_str, reply_markup=markup)


def add_goods_to_cart(message):
    user_input[message.chat.id] = message.text
    trigger = 0
    for goods in goods_info_json["objects"]:

        if user_input[message.chat.id] == goods["phone_name"]:
            cart_dict_id[goods["phone_id"]] = 0
            last_phone_id = goods["phone_id"]
            bot.send_message(message.chat.id,
                             f"How many {user_input[message.chat.id]} do you want to buy?\n"
                             f"(no more than {goods['phone_amount']} pcs.)")
            trigger = 1
            bot.register_next_step_handler(message, set_amount_of_goods, last_phone_id)

    if trigger == 0:
        bot.send_message(message.chat.id, f"Product not found. You wrote: {user_input[message.chat.id]}")
        create_order_callback(message.chat.id)


def set_amount_of_goods(message, last_phone_id):
    if int(message.text):
        for goods in goods_info_json["objects"]:
            if int(last_phone_id) == int(goods["phone_id"]) and int(message.text) <= int(goods["phone_amount"]) and int(
                    message.text) > 0:
                cart_dict_id[last_phone_id] = message.text
                create_order_callback(message.chat.id)
            elif int(last_phone_id) == int(goods["phone_id"]) and (
                    int(message.text) > int(goods["phone_amount"]) or int(message.text) <= 0):
                cart_dict_id.pop(last_phone_id, None)
                bot.send_message(message.chat.id, f"Input error")
                create_order_callback(message.chat.id)
    else:
        cart_dict_id.pop(last_phone_id, None)
        bot.send_message(message.chat.id, f"Error")
        create_order_callback(message.chat.id)


def remove_goods_from_cart(message):
    user_input[message.chat.id] = message.text
    trigger = 0
    for goods in goods_info_json["objects"]:

        if user_input[message.chat.id] == goods["phone_name"]:
            cart_dict_id[goods["phone_id"]] = 0
            cart_dict_id.pop(goods["phone_id"], None)
            bot.send_message(message.chat.id,
                             f"Product {user_input[message.chat.id]} has been removed from the cart.")
            trigger = 1
            create_order_callback(message.chat.id)

    if trigger == 0:
        bot.send_message(message.chat.id, f"Product not found. You wrote: {user_input[message.chat.id]}")
        create_order_callback(message.chat.id)


def remove_order(message):
    markup = types.InlineKeyboardMarkup()
    btn_remove_order_yes = types.InlineKeyboardButton('Yes', callback_data='remove_order_yes')
    btn_remove_order_no = types.InlineKeyboardButton('No, go back', callback_data='remove_order_no')
    markup.add(btn_remove_order_yes, btn_remove_order_no)
    bot.send_message(message, 'Are you sure you want to clear the cart?', reply_markup=markup)


def remove_order_yes(message):
    cart_dict_id.clear()
    create_order_callback(message)


def remove_order_no(message):
    create_order_callback(message)


def review_shopping_list(message):
    goods_str = get_goods_utility()[0]
    bot.send_message(message, goods_str)
    create_order_callback(message)


def finish_cart(message):
    goods_info = cart_info_utility()[0]

    bot.send_message(message.chat.id, f"{goods_info}\n\nEnter your details in the format:\n"
                                      "First name: Andrew\nLast name: Vasyliuk"
                                      "\nEmail: email@gmail.com\n"
                                      "Phone number: 0955155151\n"
                                      "Delivery address: Kyiv, Khreshchatyk 1 apt. 1\n")

    bot.register_next_step_handler(message, parse_order)


def parse_order(message):
    lines = message.text.split("\n")

    for line in lines:
        if ":" in line:
            key, value = map(str.strip, line.split(":", 1))
            parsed_data[key] = value

    markup = types.InlineKeyboardMarkup()
    btn_confirm_order_yes = types.InlineKeyboardButton('Yes', callback_data='confirm_order')
    btn_confirm_order_no = types.InlineKeyboardButton('No, go back', callback_data='cancel_order')
    markup.add(btn_confirm_order_yes, btn_confirm_order_no)

    # json_data = json.dumps(parsed_data, ensure_ascii=False)
    # print(json_data)
    # print(type(json_data))
    bot.send_message(message.chat.id, f"Your details: \n{message.text}\nDo you confirm the order?", reply_markup=markup)


def confirm_order(message):
    final_data = {
        "status_phone": 2,
        "full_price": cart_info_utility()[1],
        "billing_email": parsed_data.get('Email', ''),
        "billing_first_name": parsed_data.get('First name', ''),
        "billing_second_name": parsed_data.get('Last name', ''),
        "billing_phone_number": parsed_data.get('Phone number', ''),
        "billing_address": parsed_data.get('Delivery address', ''),
        "goods_id_dict": str(cart_dict_id)
    }

    json_data = json.dumps(final_data, ensure_ascii=False).encode('utf-8')
    print(json_data)
    post_curl(json_data, f'{main_link}api/v1/testbill/')
    print(final_data['billing_phone_number'])

    bot.send_message(message,
                     f"Your order has been successfully placed.")

    create_order_callback(message)


def cancel_order(message):
    cart_dict_id.clear()
    create_order_callback(message)


goods_info_json = get_goods_utility()[1]

bot.polling(none_stop=True)
