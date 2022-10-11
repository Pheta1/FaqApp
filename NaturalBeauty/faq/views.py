from django.contrib.auth.mixins import PermissionRequiredMixin, \
    LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from rest_framework import viewsets

from .models import Category, Faq
from .forms import StartFaqForm, UpdateFaqScoreForm, RegisterForm
from django.db.models import Q
from .serializers import CategorySerializer, FaqSerializer


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'first_category': Category.objects.first(),
            'categories': Category.objects.all()
        })

        return context


class CategoryView(TemplateView):
    template_name = 'category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(id=self.kwargs["category_id"])
        categories = Category.objects.all()
        faq_locked = Faq.objects.filter(
            category=category,
            locked=True
        )

        context.update({
            'faq_left': faq_locked[::2],
            'faq_right': faq_locked[1::2],
            'categories': categories,
            'first_category': Category.objects.first(),
            'category': category
        })

        return context


class MyView(TemplateView):
    template_name = 'my.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        my_faq = Faq.objects.filter(
            visitor=self.request.user,
            locked=True
        )

        context.update({
            'faq_left': my_faq[::2],
            'faq_right': my_faq[1::2],
            'categories': categories,
            'first_category': Category.objects.first(),
        })

        return context


class FaqUnlockedView(TemplateView, PermissionRequiredMixin):
    template_name = 'faq_unlocked.html'
    permission_required = 'faq.can_respond'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        faq_unlocked = Faq.objects.filter(
            locked=False
        )

        context.update({
            'faq_left': faq_unlocked[::2],
            'faq_right': faq_unlocked[1::2],
            'first_category': Category.objects.first(),
        })

        return context


class StartFaqView(FormView):
    form_class = StartFaqForm
    template_name = 'start_faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'first_category': Category.objects.first(),
        })

        return context

    def form_valid(self, form, *args, **kwargs):
        category = Category.objects.get(id=form.cleaned_data['category'])
        visitor_name = form.cleaned_data["visitor"] or "unknown"
        email = form.cleaned_data["email"] or "unknow@gmail.com"

        try:
            visitor = User.objects.get(
                Q(username=visitor_name) | Q(email=email)
            )
        except ObjectDoesNotExist:
            visitor = User.objects.create_user(
                username=visitor_name,
                email=email,
                is_active=False
            )

        faq = Faq.objects.create(
            category=category,
            question=form.cleaned_data["question"],
            visitor=visitor
        )

        messages.success(self.request, 'Votre question est envoyée, '
                                       'elle sera consultable lorsque la '
                                       'reponse sera disponnible')

        return HttpResponseRedirect(
            reverse('faq:category', args=(category.id,))
        )


class UpdateFaqView(FormView):
    form_class = UpdateFaqScoreForm
    template_name = 'update_faq.html'

    def get_form_kwargs(self):
        kwargs = super(UpdateFaqView, self).get_form_kwargs()
        faq = Faq.objects.get(id=self.kwargs["faq_id"])
        kwargs['faq'] = faq

        return kwargs

    def form_valid(self, form, *args, **kwargs):
        faq = Faq.objects.get(id=self.kwargs["faq_id"])
        faq.response = form.cleaned_data["response"]
        faq.locked = True
        faq.responder = self.request.user
        faq.save()

        messages.success(self.request, '{}: répondu'.format(faq.question))

        return HttpResponseRedirect(
            reverse('faq:unlock')
        )


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'first_category': Category.objects.first(),
        })

        return context

    def form_valid(self, form, *args, **kwargs):
        username = form.cleaned_data["username"]
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        try:
            user = User.objects.get(
                Q(username=username) | Q(email=email)
            )
        except ObjectDoesNotExist:
            user = User.objects.create_user(
                username=username,
                email=email
            )
        user.is_active = True
        user.password = password
        user.save()

        return HttpResponseRedirect(
            reverse('faq:my')
        )


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class FaqViewSet(viewsets.ModelViewSet):

    queryset = Faq.objects.all()
    serializer_class = FaqSerializer


# EOF
