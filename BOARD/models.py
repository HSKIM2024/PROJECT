from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.db import models

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=False,
                               related_name='author_question') #널속성 비허용
    subject = models.CharField(max_length = 100)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True,blank=True)
    recommender = models.ManyToManyField(User,related_name='recommender_question')
    def __str__(self):
        return self.subject

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=False,
                               related_name='author_answer') #널속성 비허용
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True,blank=True)
    recommender = models.ManyToManyField(User,related_name="recommender_answer")
    def __str__(self):
        return self.content

class Follow(models.Model):
    follower = models.ForeignKey(User,related_name='following',on_delete=models.CASCADE)
    following = models.ForeignKey(User,related_name='followers',on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower','following')

    def __str__(self):
        return f'{self.follower} follows {self.following}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, null=True, blank=True,default="hello")
    location = models.CharField(max_length=30, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to="profile_pics/", null=True, blank=True)

    def __str__(self):
        return self.user.username


