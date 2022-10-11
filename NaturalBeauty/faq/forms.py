from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm


from .models import Question, Response


class QuestionForm(ModelForm):

    class Meta:
        model = Question
        fields = ['question', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class UserForm(forms.Form):
    visitor = forms.CharField(
        label='Nom/pseudo',
        required=False
    )
    email = forms.EmailField(
        label='email',
        required=False
    )


class ResponseForm(ModelForm):
    class Meta:
        model = Response
        fields = ['response']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

# EOF
