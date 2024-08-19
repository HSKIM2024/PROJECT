from django import forms
from  BOARD.models import Question,Answer,Profile

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject','content']
        labels = {
            'subject': '제목',
            'content': '내용',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['subscript','profile_image']
