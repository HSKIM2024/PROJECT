from django.shortcuts import render,redirect,get_object_or_404
from django.utils import timezone
from .models import Question,Answer,Profile
from BOARD.forms import QuestionForm,AnswerForm,ProfileForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q,Count
from django.contrib.auth import logout
from django.contrib.auth import login,authenticate
from BOARD.forms import UserForm,UserCreationForm
from django.http import JsonResponse
from django.contrib.auth.models import User
from.models import Follow

def LOGOUT_VIEW(request):
    logout(request)
    return redirect("index")

def SIGNUP_VIEW(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password) #사용자인증
            login(request, user) #로그인
            return redirect("index")
    else:
        form = UserForm()
    return render(request, "BOARD/signup.html", {"form":form})

def index(request):
    page = request.GET.get('page','1') #페이지
    keyword = request.GET.get('keyword','') #검색어
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

@login_required(login_url='login_view')
def follow_user(request,user_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error':'Authentication required'},status=403)
    user_to_follow = get_object_or_404(User,id=user_id)

    if user_to_follow == request.user:
        return JsonResponse({'error':'You cannot follow yourself'},status=400)

    follow,created = Follow.objects.get_or_create(follower=request.user,following=user_to_follow)

    if created:
        return JsonResponse({'message':f'You are now following {user_to_follow.username}'},status=201)
    else:
        return JsonResponse({'message':'You are already following this user'},status=400)
@login_required(login_url='login_view')
def unfollow_user(request,user_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error':'Authentication required'},status=403)
    user_to_unfollow = get_object_or_404(User,id=user_id)

    if user_to_unfollow == request.user:
        return JsonResponse({'error':'You cannot unfollow yourself'},status=400)

    try:
        follow = Follow.objects.get(follower=request.user, following=user_to_unfollow)
        follow.delete()
        return JsonResponse({'message':f'You have unfollowed {user_to_unfollow.username}'},status=200)
    except Follow.DoesNotExist:
        return JsonResponse({'error':'You are not following this user'},status=400)

@login_required(login_url='login_view')
def view_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    return render(request,'BOARD/profile_view.html',{'profile': profile})

@login_required(login_url='login_view')
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request,'BOARD/profile_update.html',{'form': form})

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save,sender=User) #기존사용자로 로그인했을때, 프로필을 디폴트로 채워줌
def save_user_profile(sender,instance,**kwargs):
    profile,created = Profile.objects.get_or_create(user=instance,defaults={
        'bio': 'hello',
        'location':'Not Added',
        'birth_date':None,
        'profile_image': None,
    })
    profile.save()

def user_login(request):
    #기존 로그인 로직
    if request.method == 'POST':
    # 사용자인증및로그인처리

    #로그인성공시 프로필생성확인
        user = request.user
        Profile.objects.get_or_create(user=user)
        return redirect('index') #로그인후 리다이렉트할페이지
    return render(request,'BOARD/login.html')

def user_profile(request,username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user) #프로필모델이있는경우
    #프로필데이터를 템플릿에 전달
    return render(request, 'BOARD/user_profile.html',{'profile': profile,'user': user})


