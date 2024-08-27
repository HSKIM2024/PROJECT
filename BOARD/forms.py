from django import forms
from BOARD.models import Question, Answer, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject','content']
        labels = {
            'subject': '게시물제목',
            'content': '게시물내용',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','location','birth_date','profile_image']