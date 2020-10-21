from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse

from .models import User,User_profile,Poem

import json

from markdown2 import Markdown

markdowner = Markdown()


def content_valid_check(content):
    if len(content) == 0:
        return False
    check  = 0
    for i in content:
        if i != ' ':
            check = 1
    if check == 0:
        return False
    else:
        return True                


def handle_json_request(request,data):
    
    if data['type'] == 'edit-profile':
        try:
            user_requested =  User.objects.get(pk= int(data['pk']))
            if user_requested != request.user :
                return 
            user_requested_profile = User_profile.objects.get(user=user_requested)
            user_requested_profile.name = data['name']
            user_requested_profile.about = data['about']
            user_requested_profile.save()

        except User.DoesNotExist:
            return 

# index view
def index(request):
    return render(request,"poems/index.html")

# login view 
def login_view(request):

    if request.method == 'POST':

        # Attempt to sign in user 

        username = request.POST["username"] 
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)   

        # Check if authentication was a success
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"poems/login.html",{ "message":"Invalid username and/or password."})  
    else:
        return render(request,'poems/login.html')          

# log-out view
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index")) 

# sign-up view
def register(request):

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        firstname =request.POST["firstname"]
        lastname =request.POST["lastname"]


        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request,"poems/register.html",{
            "message": "Passwords Must match."
            })
        
        #  Attempt to create new user
        try:
            user = User.objects.create_user(username,email,password)
            user.save()
            user_profile=User_profile(user=user)
            user_profile.about = "I'll let my poems speak for me."
            user_profile.save()
        except IndentationError:
            return render(request,"poems/register.html",{
            "message": "Sorry,username already taken."
            })       

        login(request,user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request,"poems/register.html")       

# User profile view
def user_view(request,pk):

    if request.method == 'PUT':
        data = json.loads(request.body)
        handle_json_request(request,data)

    if request.method == 'POST' and request.FILES['file']:
        x = User_profile.objects.get(user=request.user)
        x.profile_image = request.FILES['file']
        x.save()

    try:
        requested_user = User.objects.get(pk=pk)

        # check if the user if trying to view thier own profile
        self_view = False
        if requested_user == request.user:
            self_view = True


        return render(request,"poems/profile.html",{
            "requested_user":requested_user,
            'self_view':self_view

        }) 

    except User.DoesNotExist:
        return HttpResponseRedirect(reverse("index")) 

@login_required
def create(request):
    if request.method == "POST":
        if request.POST['part'] == 'part-1':
            content = request.POST['content']
            if content_valid_check(content):
                poem = Poem(user=request.user,content=content)
                poem.save()
                return render(request,'poems/create_1.html',{'message':'The content of your poem saved..','pk':poem.pk})
            else:
                return render(request,'poems/create.html',{'message':'You submitted an empty form..'})  
        if request.method == "POST":
            if request.POST['part'] == 'part-2':
                pk = int(request.POST['pk'])
                title = request.POST['title']
                discription = request.POST['discription']
                publish = request.POST['publish']
                try:
                    poem = Poem.objects.get(pk=pk)
                except poem.DoesNotExist:
                    pass    
                if content_valid_check(title):
                    poem.title = title
                if content_valid_check(discription):
                    poem.discription = discription
                if publish == 'Yes':
                    poem.published =True
                else:
                    poem.published = False        
                poem.save()
                return HttpResponseRedirect(reverse("index")) 
                      


    return render(request,'poems/create.html')        

def poem_view(request,pk):
    try:
        poem =  Poem.objects.get(pk=pk)
        content = markdowner.convert(poem.content)
    except Poem.DoesNotExist:
        return HttpResponseRedirect(reverse("index")) 
        
    return render(request,'poems/poem_view.html',{'poem':poem,'content':content})
