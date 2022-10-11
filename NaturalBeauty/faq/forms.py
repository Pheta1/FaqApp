from django import forms

from faq.models import Category


class StartFaqForm(forms.Form):

    question = forms.CharField(
        label='Votre question',
        required=True
    )
    visitor = forms.CharField(
        label='Nom/pseudo',
        required=False
    )
    email = forms.EmailField(
        label='email',
        required=False
    )
    category = forms.ChoiceField(
        label='Category',
        choices=[
            (category.id, category.name) for category in Category.objects.all()
        ],
        required=True
    )


class UpdateFaqScoreForm(forms.Form):
    def __init__(self, faq, *args, **kwargs):
        super(UpdateFaqScoreForm, self).__init__(*args, **kwargs)
        self.fields["question"].initial = faq.question
        self.fields["visitor"].initial = faq.visitor.username
        self.fields["email"].initial = faq.visitor.email
        self.fields["category"].initial = faq.category.name

    question = forms.CharField(
        label='Votre question',
        required=True
    )
    visitor = forms.CharField(
        label='Nom/pseudo',
        required=False
    )
    email = forms.EmailField(
        label='email',
        required=False
    )
    response = forms.CharField(
        label='Réponse',
        required=True
    )
    category = forms.CharField(
        label='Category',
        required=True
    )


class RegisterForm(forms.Form):

    username = forms.CharField(
        label='Votre Nom',
        required=True
    )
    password = forms.CharField(
        label='Votre mot de passe',
    )
    email = forms.EmailField(
        label='email',
    )

# EOF
