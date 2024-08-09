# OnlineCatalog

Welcome to the "Online Store" project repository. This project is a modern and user-friendly e-commerce website that offers a wide range of products and integrated features for the convenience of both customers and administrators.

- [Description](#description)
- [Demo](#demo)
- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)


## Description
The "Online Store" is a fully-featured web application that allows users to browse and purchase products online. The store supports various product categories and account management for customers and administrators.

## Demo
- Web Application: [OnlineCatalog](http://slowtown.pythonanywhere.com)
- Telegram Bot: [OnlineCatalog Bot](https://t.me/OnlineCatal0g_bot)

## Features

- **Product Catalog:** Browse, filter, and sort products by categories.
- **Shopping Cart:** Add and remove products from the cart, and proceed to checkout.
- **User Accounts:** Register, log in, and manage profiles and order history.
- **Admin Panel:** Manage products, categories, orders, and users.
- **Site Search:** Convenient product search by name and keywords.
- **Smart Pages:** Create and manage smartpages from adminpanel. 

## Technologies

- **Frontend:** HTML, CSS, Bootstrap
- **Backend:** Python, Django, DRF
- **Database:** MySQL
- **Hosting:** PythonAnywhere


## Installation

### Step 1: Clone the repository
The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/slowtown1947/OnlineCatalog
$ cd OnlineCatalog
```

### Step 2: Create a virtual environment
Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv --no-site-packages env
$ source env/bin/activate
```

### Step 3: Install dependencies
Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```

### Step 4: Configure the database
To run the project, you need to install MySQL on your computer and create an empty database. Then, edit the OnlineCatalog/settings.py file to fill the DATABASES section with the necessary information:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'name_of_your_database',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',  # or the hostname where your MySQL server is running
        'PORT': '3306',  # or the port on which your MySQL server is listening
    }
}
```

### Step 5: Apply migrations
After that, you need to make migrations and migrate them by following these commands:

```sh
(env)$ python manage.py makemigrations
(env)$ python manage.py migrate
```

### Step 6: Run the server
After that, you can run the server and the Telegram bot:

```sh
(env)$ python manage.py runserver & python bot.py
```
