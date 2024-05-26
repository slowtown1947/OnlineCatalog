My student project about Django and DRF basic knowledge.
This project is simple online catalog for any goods you want.
Also contains telegram bot for checking orders info and creating new orders.

Run with:
python manage.py runserver & python bot.py

Project is hosted by link:
http://slowtown.pythonanywhere.com
And telegram bot is hosted:
https://t.me/OnlineCatal0g_bot

OnlineCart sample application
Setup

The first thing to do is to clone the repository:

$ git clone https://github.com/slowtown1947/OnlineCatalog
$ cd OnlineCatalog

Create a virtual environment to install dependencies in and activate it:

$ virtualenv2 --no-site-packages env
$ source env/bin/activate

Then install the dependencies:

(env)$ pip install -r requirements.txt

Note the (env) in front of the prompt. This indicates that this terminal session operates in a virtual environment.

Once pip has finished downloading the dependencies:

To run the project you need to install mysql to your computer and create empty database.
Then go to OnlineCatalog/settings.py and fix the database part so that it is filled with the information you need.

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

After that you need to make migrations and migrate them by following this commands

(env)$ python manage.py makemigrations
(env)$ python manage.py migrate

After that you can runserver by this command

(env)$ python manage.py runserver & python bot.py

And navigate to http://127.0.0.1:8000.



