from django.contrib import admin
from .models import Question,Answer,Profile

class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']
class AnswerAdmin(admin.ModelAdmin):
    search_fields = ['content']

class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['user']

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Profile)
