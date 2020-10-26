from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse

from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

from .models import User,User_profile,Poem,Comment,Library

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
    elif data['type'] == 'comment' :
        try:
            user_requested =  User.objects.get(pk=request.user.pk)
        except User.DoesNotExist:
            return
        try:
            poem =  Poem.objects.get(pk= data['pk'])
        except Poem.DoesNotExist:
            return
        comment = Comment(user = user_requested,poem= poem,content=data['comment'])      
        comment.save()

    elif data['type'] == 'remove_library':
        try:
            requested_user = User.objects.get(pk= request.user.pk)
        except User.DoesNotExist:
            return 
        try:
            requested_poem = Poem.objects.get(pk=data['pk']) 
        except Poem.DoesNotExist:
            return
        try:
            l = Library.objects.get(user=requested_user,poem=requested_poem)
            l.delete()
        except Library.DoesNotExist:
            return
    elif data['type'] == 'add_library':
        try:
            requested_user = User.objects.get(pk= request.user.pk)
        except User.DoesNotExist:
            return 
        try:
            requested_poem = Poem.objects.get(pk=data['pk']) 
        except Poem.DoesNotExist:
            return
        try:
            l = Library.objects.get(user=requested_user,poem=requested_poem)      
            return
        except Library.DoesNotExist:
            l = Library(user=requested_user,poem=requested_poem) 
            l.save()
            return

def pignate(request,posts):
    page = request.GET.get('page',1)
    paginator = Paginator(posts,10)

    try:
        post_page = paginator.page(page)
    except PageNotAnInteger:
        post_page  = paginator.page(1)
    except EmptyPage:
        post_page = paginator.page(paginator.num_pages)

    return post_page   

# index view
def index(request):
    all_poems = Poem.objects.all().filter(published=True).order_by('-created_on')
    return render(request,"poems/index.html",{'posts':pignate(request,all_poems)})

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

        poems = Poem.objects.all().filter(user=requested_user)

        nav  = True if len(poems) !=0 else False

        return render(request,"poems/profile.html",{
            "requested_user":requested_user,
            'self_view':self_view,'posts':pignate(request,poems),'nav':nav

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
                    poem = Poem.objects.get(pk=pk,user=request.user)
                except poem.DoesNotExist:
                    return HttpResponseRedirect(reverse("index")) 
                if content_valid_check(title):
                    poem.title = title
                if content_valid_check(discription):
                    poem.discription = discription
                if publish == 'Yes':
                    poem.published =True
                else:
                    poem.published = False    
                try:
                    poem.cover_image = request.FILES['file'] 
                except:
                    pass       
                poem.save()
                return HttpResponseRedirect(reverse("index")) 
                      


    return render(request,'poems/create.html')        

def poem_view(request,pk):
    if request.method == 'PUT':
        data = json.loads(request.body)
        handle_json_request(request,data)

    try:
        poem =  Poem.objects.get(pk=pk)
        content = markdowner.convert(poem.content)
    except Poem.DoesNotExist:
        return HttpResponseRedirect(reverse("index")) 

    user_logged = True
    library = False
    try:
        user = User.objects.get(pk= request.user.pk)
    except User.DoesNotExist:
        user_logged = False
        
    if user_logged:
        for each in user.library.all():
            if each.poem.pk == pk:
                library = True
                break



    comments = Comment.objects.all().filter(poem=poem).order_by('-commented_on')[:10]

    return render(request,'poems/poem_view.html',{'poem':poem,'content':content,'comments':comments,'user_logged':user_logged,'library':library})


@login_required
def library_view(request):
    poems = Library.objects.all().filter(user=request.user).order_by('-added_on')
    nav  = True if len(poems) !=0 else False
    return render(request,'poems/library.html',{'posts':pignate(request,poems),'nav':nav})
