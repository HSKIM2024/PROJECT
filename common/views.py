from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.contrib.auth import login,authenticate
from common.forms import UserForm
from BOARD.forms import ProfileForm
from django.contrib.auth.decorators import login_required

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
    return render(request, "common/signup.html",{"form":form})