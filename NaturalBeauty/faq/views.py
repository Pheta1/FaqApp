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

from .models import Category, Question, Response
from .forms import RegisterForm, QuestionForm, UserForm, ResponseForm
from django.db.models import Q
from .serializers import CategorySerializer, ResponseSerializer, QuestionSerializer


class HomeView(TemplateView):
    """View used by the visitor to navigate through the site """

    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'first_category': Category.objects.first(),
            'categories': Category.objects.all()
        })

        return context


class UserView(TemplateView):
    """The view used by a member: shows all the questions the user requested"""

    template_name = 'user_faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        user_question = Question.objects.filter(
            visitor=self.request.user,
            locked=True
        )

        context.update({
            'faq_left': user_question[::2],
            'faq_right': user_question[1::2],
            'categories': categories,
            'first_category': Category.objects.first(),
        })

        return context


class FaqView(TemplateView):
    """View used by the visitor show all faq with response"""

    template_name = 'category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(id=self.kwargs["category_id"])
        categories = Category.objects.all()
        question_locked = Question.objects.filter(
            category=category,
            locked=True
        )

        context.update({
            'faq_left': question_locked[::2],
            'faq_right': question_locked[1::2],
            'categories': categories,
            'first_category': Category.objects.first(),
            'category': category
        })

        return context


class FaqUnlockedView(TemplateView, PermissionRequiredMixin):
    """View used by client show all faq with no response """

    template_name = 'faq_unlocked.html'
    permission_required = 'faq.can_respond'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        question_unlocked = Question.objects.filter(
            locked=False
        )

        context.update({
            'faq_left': question_unlocked[::2],
            'faq_right': question_unlocked[1::2],
            'first_category': Category.objects.first(),
        })

        return context


class StartFaqView(FormView):
    """View used by the visitor to ask a question """

    form_class = QuestionForm
    template_name = 'start_faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'first_category': Category.objects.first(),
            'visitor_form': UserForm
        })

        return context

    def form_valid(self, form, *args, **kwargs):
        visitor_form = UserForm(self.request.POST)

        if visitor_form.is_valid():
            username = visitor_form.cleaned_data["visitor"] or "unknown"
            email = visitor_form.cleaned_data["email"] or "unknown@gmail.com"

            try:
                visitor = User.objects.get(
                    Q(username=username) | Q(email=email)
                )
            except User.DoesNotExist:
                visitor = User.objects.create_user(
                    username=username,
                    email=email,
                    is_active=False
                )

            question = form.save()
            question.visitor = visitor
            question.save()

            messages.success(
                self.request,
                'Votre question est envoyée, '
                'elle sera consultable lorsque la réponse sera disponible'
            )
        else:
            messages.error(
                self.kwargs,
                "{}".format(visitor_form.errors)
            )

        return HttpResponseRedirect(
            reverse('faq:category', args=(question.category.id,))
        )


class UpdateFaqView(FormView):
    """View used by the client to response a faq """

    form_class = ResponseForm
    template_name = 'update_faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = Question.objects.get(id=self.kwargs["faq_id"])

        context.update({
            'first_category': Category.objects.first(),
            'question': question,

        })

        return context

    def form_valid(self, form, *args, **kwargs):
        question = Question.objects.get(id=self.kwargs["faq_id"])
        response = form.save()
        response.responder = self.request.user
        response.save()
        question.response.add(response)

        messages.success(
            self.request, '{}: répondu'.format(question.question)
        )

        return HttpResponseRedirect(
            reverse('faq:unlock')
        )


class RegisterView(FormView):
    """View used by the visitor to register """

    form_class = RegisterForm
    template_name = 'register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'first_category': Category.objects.first(),
        })

        return context

    def form_valid(self, form, *args, **kwargs):
        form.save()

        return HttpResponseRedirect(
            reverse('faq:my')
        )


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ResponseViewSet(viewsets.ModelViewSet):

    queryset = Response.objects.all()
    serializer_class = ResponseSerializer


class QuestionViewSet(viewsets.ModelViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionUnlockViewSet(viewsets.ModelViewSet):

    queryset = Question.objects.filter(locked=False)
    serializer_class = QuestionSerializer


# EOF
