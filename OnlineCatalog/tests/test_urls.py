from django.test import SimpleTestCase
from django.urls import reverse, resolve
from phones.views import cart, homepage, edit_page, view_phone


class TestUrls(SimpleTestCase):

    def test_homepage_url_is_resolved(self):
        url = reverse('homepage')
        self.assertEquals(resolve(url).func, homepage)

    def test_view_phone_url_is_resolved(self):
        url = reverse('view_phone', args=['20'])
        self.assertEquals(resolve(url).func, view_phone)

    def test_cart_url_is_resolved(self):
        url = reverse('cart')
        self.assertEquals(resolve(url).func, cart)

    def test_edit_page_url_is_resolved(self):
        url = reverse('edit_page')
        self.assertEquals(resolve(url).func, edit_page)
