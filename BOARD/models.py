from django.db import models
from django.contrib.auth.models import User

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

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    subscript = models.CharField("유저소개문",max_length=200,blank=True)
    profile_image = models.ImageField("유저이미지",upload_to='profile_images/',blank=True,null=True)