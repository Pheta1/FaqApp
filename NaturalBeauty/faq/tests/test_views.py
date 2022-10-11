# flake8: noqa
import json
from django.test import Client

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from model_bakery import baker

from faq.models import Faq, Category


class HomeViewTestCase(TestCase):

    def setUp(self):
        self.category1 = Category.objects.create(
            name="cheveux",
            description="Astuces pour retrouver des cheveux sains ")
        self.category2 = Category.objects.create(
            name="visage",
            description="Astuces pour une peau bien hydratée"
        )
        image_path = "{}/category/visage.jpeg".format(settings.BASE_DIR)
        self.category2.image = SimpleUploadedFile(
            name='visage.jpeg',
            content=open(bytes(image_path, encoding='utf-8'), 'rb').read(),
            content_type='visage.jpeg'
        )
        self.category1.image = SimpleUploadedFile(
            name='visage.jpeg',
            content=open(bytes(image_path, encoding='utf-8'), 'rb').read(),
            content_type='visage.jpeg'
        )
        self.category1.save()
        self.category2.save()
        self.category1.refresh_from_db()
        self.category2.refresh_from_db()

    def test_context_data(self):
        response = self.client.get(reverse('faq:home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['first_category'], self.category1)


class MyViewTestCase(TestCase):
    def setUp(self):
        self.user = baker.make(User)
        self.faq = Faq.objects.create(
            question="this is a question",
            category=baker.make(Category),
            visitor=self.user
        )

    def test_login_required(self):
        response = self.client.get(reverse('faq:my'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "/login/?next=/my",
            target_status_code=200,
            fetch_redirect_response=True
        )


class FaqUnlockedViewTestCase(TestCase):
    def setUp(self):
        self.user = baker.make(User)
        self.faq = Faq.objects.create(
            question="this is a question",
            category=baker.make(Category),
            visitor=self.user
        )

    def test_login_required(self):
        response = self.client.get(reverse('faq:unlock'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/?next=/unlock")


class UpdateFaqViewTestCase(TestCase):
    def setUp(self):
        self.faq = Faq.objects.create(
            category=baker.make(Category),
            question="this is a question",
            visitor=baker.make(User)
        )
        self.faq.save()
        self.faq.refresh_from_db()

    def test_update_faq(self):
        url_start = reverse('faq:update', args=(self.faq.id,))
        data = {
            'visitor': self.faq.visitor.username,
            'email': self.faq.visitor.email,
            'category': self.faq.category.name,
            'question': self.faq.question,
            'response': "this is a response",
        }
        response = self.client.post(
            url_start,
            data=data,
            follow=True
        )
        self.faq.refresh_from_db()
        self.assertEqual(response.status_code, 200)


class RegisterViewTestCase(TestCase):

    def test_csrf(self):
        url = reverse('faq:register')
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_register_post(self):
        url_register = reverse('faq:register')
        data = {
            'username': 'test1',
            'email': 'test1@gmail.com',
            'password': "password"
        }
        response = self.client.post(
            url_register,
            data=data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.count())
# EOF
