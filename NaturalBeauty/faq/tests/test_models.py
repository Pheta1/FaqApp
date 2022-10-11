
from django.contrib.auth.models import User
from django.test import TestCase
from faq.models import Category, Faq
from model_bakery import baker


class CategoryTestCase(TestCase):
    def setUp(self):
        Category.objects.create(
            name="cheveux",
            description="Comment retrouver des cheveux sains ")
        Category.objects.create(
            name="visage",
            description="Astuces pour une peau bien hydratée"
        )

    def test_first_category(self):
        category = Category.objects.first()
        self.assertEqual(category.name, "cheveux")


class FaqTestCase(TestCase):

    def setUp(self):
        self.faq = Faq.objects.create(
            category=baker.make(Category),
            question="quels soin correspond à un cheveux de type 2c",
            visitor=baker.make(User)
        )

    def test_locked(self):
        self.faq.response = "this is a response of the question"
        self.faq.responder = baker.make(User)
        self.faq.locked = True
        self.faq.save()
        self.faq.refresh_from_db()
        self.assertEqual(self.faq.locked, True)
