from django.shortcuts import render,redirect
from django.utils import timezone
from .models import Question,Answer
from django.http import HttpResponseNotAllowed
from .forms import QuestionForm,AnswerForm

def index(request):
    QList = Question.objects.order_by('-create_date')
    context = {"QList": QList}
    return render(request,"BOARD/QList.html",context)

def detail(request,question_id):
    QDetail = Question.objects.get(id =question_id)
    context = {"QDetail": QDetail}
    return render(request, "BOARD/QDetail.html",context)

# def answer_create(request,question_id):
#     question = Question.objects.get(id=question_id)
#     if request.method == "POST":
#         form = AnswerForm(request.POST)
#         if form.is_valid():
#             answer = form.save(commit=False)
#             answer.create_date = timezone.now()
#             answer.question = question
#             answer.save()
#             return redirect("detail",question_id=question.id)
#         else:
#             return redirect("detail",question_id=question_id)
#     else:
#         return HttpResponseNotAllowed("Only POST method is allowed")
#     context = {"question": question,"form": form}
#     return render(request, "BOARD/QDetail.html",context)
def answer_create(request,question_id):
    question = Question.objects.get(id=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect("detail",question_id=question.id)
    else:
        form = AnswerForm()
    context = {"form": form}
    return render(request, "BOARD/AForm.html",context)

def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'BOARD/QForm.html',context)