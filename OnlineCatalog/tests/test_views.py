from django.test import TestCase, Client
from django.urls import reverse
from phones.models import PhoneModel, Pages, Baskets, Billings
from django.contrib.auth.models import User
from phones.views import cart, get_cart


class LoginViewTest(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_view_rendering(self):
        response = self.client.get(reverse('login_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_successful_login(self):
        data = {'username': self.username, 'password': self.password}
        response = self.client.post(reverse('login_user'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('homepage'))

    def test_unsuccessful_login(self):
        data = {'username': self.username, 'password': 'wrongpassword'}
        response = self.client.post(reverse('login_user'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        # self.assertContains(response, "Неправильне ім'я користувач або пароль.")


class CartViewTest(TestCase):

    # def test_cart_view_rendering(self):
        #
        # response = self.client.get(reverse("cart"))
        # self.assertEqual(response.status_code, 301)
        # self.assertTemplateUsed(response, 'cart.html')

    def test_get_cart_view_rendering(self):
        response = self.client.get(reverse("get_cart"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart.html')


    # self.assertEqual(response.status_code, 200)  # check 200 OK response
    # wines = response.context['wines']  # this is the list of wines you included in the context
    # # check that wines is as you expected.
    # for wine in wines:
    #     # All wines should be active
    #     self.assertTrue(wine.is_active)
