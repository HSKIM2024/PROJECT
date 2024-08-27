from django.contrib import admin
from django.urls import path, include

from BOARD import views
import BOARD.views
from django.contrib.auth import views as AUTH_VIEW
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('BOARD/',BOARD.views.index,name="index"),
    path('',BOARD.views.index,name="index"),
    path('<int:question_id>/',BOARD.views.detail,name="detail"),
    path('answer/create/<int:question_id>/',BOARD.views.answer_create, name="answer_create"),
    path('answer/modify/<int:answer_id>/',BOARD.views.answer_modify, name="answer_modify"),
    path('answer/delete/<int:answer_id>/',BOARD.views.answer_delete, name="answer_delete"),
    path('question/create/', BOARD.views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/', BOARD.views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/',BOARD.views.question_delete, name='question_delete'),
    path('BOARD/login/', AUTH_VIEW.LoginView.as_view(template_name='BOARD/login.html'), name='login_view'),
    path('BOARD/logout/',BOARD.views.LOGOUT_VIEW,name='logout_view'),
    path('BOARD/signup/',BOARD.views.SIGNUP_VIEW, name="signup_view"),
    path('question/recommend/<int:question_id>/',BOARD.views.question_recommend, name='question_recommend'),
    path('answer/recommend/<int:answer_id>/',BOARD.views.answer_recommend, name='answer_recommend'),
    path('accounts/', include('allauth.urls')),
    path('follow/<int:user_id>/',views.follow_user,name='follow_user'),
    path('unfollow/<int:user_id>/',views.unfollow_user,name='unfollow_user'),
    path('profile/update/',views.update_profile,name='update_profile'),
    path('profile/view/',views.view_profile,name='view_profile'),
    path('profile/<str:username>/',views.user_profile,name='user_profile')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
