from django.shortcuts import render,redirect
from django.utils import timezone
from .models import Question,Answer
from django.http import HttpResponseNotAllowed
from .forms import QuestionForm,AnswerForm,ProfileForm
from common.forms import UserForm,UserCreationForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

def index(request):
    page = request.GET.get('page','1')
    keyword = request.GET.get('keyword','')
    QList = Question.objects.order_by('-create_date')
    if keyword:
        QList = QList.filter(
            Q(subject__icontains=keyword) | #제목검색
            Q(content__icontains=keyword) | #내용검색
            Q(answer__content__icontains=keyword) | #답변내용검색
            Q(author__username__icontains=keyword) | #질문유저검색
            Q(answer__author__username__icontains=keyword) #답변유저검색
        ).distinct()
    paginator = Paginator(QList,10)
    page_object = paginator.get_page(page)
    context = {"QList": page_object,"page":page,"keyword":keyword}
    return render(request,"BOARD/QList.html",context)

def detail(request,question_id):
    QDetail = Question.objects.get(id =question_id)
    context = {"QDetail": QDetail}
    return render(request, "BOARD/QDetail.html",context)

@login_required(login_url='login_view')
def answer_create(request,question_id):
    question = Question.objects.get(id=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect("detail",question_id=question.id)
    else:
        form = AnswerForm()
    context = {"form": form}
    return render(request, "BOARD/AForm.html",context)

@login_required(login_url='login_view')
def answer_modify(request,answer_id):
    answer = Answer.objects.get(id=answer_id)
    if request.user != answer.author:
        messages.error(request,"수정권한이 없습니다.")
        return redirect("detail",question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect("detail",question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {"answer": answer, "form": form}
    return render(request, "BOARD/AForm.html",context)

@login_required(login_url='login_view')
def answer_delete(request,answer_id):
    answer = Answer.objects.get(id=answer_id)
    if request.user != answer.author:
        messages.error(request,"삭제권한이 없습니다.")
    else:
        answer.delete()
    return redirect("detail",question_id=answer.question.id)


@login_required(login_url='login_view')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'BOARD/QForm.html',context)

@login_required(login_url='login_view')
def question_modify(request,question_id):
    question = Question.objects.get(id=question_id)
    if request.user != question.author:
        messages.error(request,"수정권한이 없습니다.")
        return redirect('detail',question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST,instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect('detail',question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, "BOARD/QForm.html",context)

@login_required(login_url='login_view')
def question_delete(request,question_id):
    question = Question.objects.get(id=question_id)
    if request.user != question.author:
        messages.error(request,"삭제권한이 없습니다.")
        return redirect('detail',question_id=question.id)
    question.delete()
    return redirect('index')

@login_required(login_url='login_view')
def question_recommend(request,question_id):
    question = Question.objects.get(id=question_id)
    if request.user == question.author:
        messages.error(request,"본인이 작성한 글은 추천할 수 없습니다.")
    else:
        question.recommender.add(request.user)
    return redirect("detail",question_id=question.id)

@login_required(login_url='login_view')
def answer_recommend(request,answer_id):
    answer = Answer.objects.get(id=answer_id)
    if request.user == answer.author:
        messages.error(request,"본인이 작성한 글은 추천할 수 없습니다.")
    else:
        answer.recommender.add(request.user)
    return redirect("detail",question_id=answer.question.id)

# @login_required(login_url='login_view')
# def user_mypage_update(request):
#     if request.method == 'POST':
#         form = UserUpdateForm(request.POST, instance=request.user)
#         profileform = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
#
#         if form.is_valid() and profileform.is_valid():
#             form.save()
#             profileform.save()
#             messages.success(request,"프로필이 업데이트 되었습니다!")
#             return redirect("/user/mypage")
#     else:
#         user_form = UserForm(instance=request.user)
#         profile_form = ProfileForm(instance=request.user.profile)
#     return render(request,'user/mypage_update.html',{'form':user_form,'profileform':profile_form})
