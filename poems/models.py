from django.contrib.auth.models import AbstractUser

from django.db import models

# User model auth.

class User(AbstractUser):
    pass

class User_profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(blank= True,default="anonymous",max_length=20)
    about = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='images/',null=True,blank=True)

class Poem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='poems')
    title = models.CharField(blank=True,default='The Untitled Poem',max_length=30)
    discription = models.TextField(blank=True)
    content = models.TextField()
    cover_image =  models.ImageField(upload_to='images/',default='images/stock.jpg')
    published = models.BooleanField(default=False)
    created_on =  models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comment')
    poem = models.ForeignKey(Poem,on_delete=models.CASCADE,related_name='comments')
    content = models.TextField(blank=False)
    commented_on =  models.DateTimeField(auto_now_add=True)

class Library(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='library')
    poem = models.ForeignKey(Poem,on_delete=models.CASCADE)
    added_on =  models.DateTimeField(auto_now_add=True)