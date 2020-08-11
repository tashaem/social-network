import json 

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import JsonResponse

from .models import *


def index(request):
    """Main Feed / Home Page"""

    if request.method=="POST":

        if 'newpostbutton' in request.POST:

            # Retrieves HTML form data
            content = request.POST["newpost"]

            # Updates DB
            newpost = Post(user=request.user, content=content)
            newpost.save()

    # Retrieves posts from DB
    all_posts = Post.objects.all().order_by('-timestamp')
    
    # Pagination settings
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html",{
        "posts": page_obj
    })

@login_required
def profile(request, username):
    """Profile Page"""

    # Retrieves user/profile/posts info from DB
    currentuser = User.objects.get(username=username)
    currentprofile= Profile.objects.get(user=currentuser)
    personalprofile=Profile.objects.get(user=request.user)
    user_posts = Post.objects.filter(user=currentuser).order_by('-timestamp')

    # Pagination settings
    paginator = Paginator(user_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Follow / Unfollow feature

    followed= False

    if request.method=="POST":

        if 'followbutton' in request.POST:
            currentprofile.follower.add(request.user)
            currentprofile.save()
            personalprofile.following.add(currentuser)
            personalprofile.save()
            
        elif 'unfollowbutton' in request.POST:
            currentprofile.follower.remove(request.user)
            currentprofile.save()
            personalprofile.following.remove(currentuser)
            personalprofile.save()

    if currentuser == request.user:
        personalprofile = True
    else:
        personalprofile = False
        
        try:
            followship = Profile.objects.get(user=currentuser, follower=request.user)
        except Profile.DoesNotExist:
            followship = None
        
        if followship!=None:
            followed = True

    return render(request, "network/profile.html",{
        "posts":page_obj,
        "currentuser":currentuser,
        "currentprofile":currentprofile,
        "personalprofile":personalprofile,
        "followed":followed
    })

@login_required
def following(request):
    """Following/Secondary Feed"""

    if request.method=="POST":
        if 'newpostbutton' in request.POST:

            # Retrieves HTML form data
            content = request.POST["newpost"]

            # Updates DB
            newpost = Post(user=request.user, content=content)
            newpost.save()


    followed_posts = []

    try: 
        # Retrieving followed users from DB
        personalprofile = Profile.objects.get(user=request.user)
        followed_users = User.objects.filter(following=personalprofile)
    except User.DoesNotExist:
        followed_users = None

    # Retrieving posts from DB
    followed_posts = Post.objects.filter(user__in=followed_users).order_by('-timestamp')

    # Pagination settings
    paginator = Paginator(followed_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/index.html",{
        "posts": page_obj
    })

@login_required
@csrf_exempt
def edit(request):
    """Edits Posts (Response to JS fetch)"""

    if request.method =="POST":

        # Saving JS form data
        post_id = int(request.POST.get('id'))
        post_newcontent = request.POST.get('content')

        try:
            post = Post.objects.get(id=post_id)

            if post.user == request.user:

                # Updates the DB
                post.content = post_newcontent
                post.save()

                return JsonResponse({}, status=201)

        except:
            return JsonResponse({},status=404)

    else:
        # Returns 400 Error if it isn't a POST request
        return JsonResponse({}, status=400)
        
@login_required
@csrf_exempt
def like(request):
    """Like Feature (Response to JS fetch)"""

    if request.method=="POST":

        # Saving JS form data
        post_id = int(request.POST.get('id'))

        try: 
            post = Post.objects.get(id=post_id)

            # Adds / removes 'like' from DB
            if request.user in post.likers.all():
                post.likers.remove(request.user)
                post.save()
                liked = False
            else:
                post.likers.add(request.user)
                post.save()
                liked = True
        
            return JsonResponse({"liked": liked, "count": post.likers.count(), "status": '201'})

        except:
            return JsonResponse({'error': "Page not found", "status": 404})

    else:
        # Returns 400 Error if it isn't a POST request
        return JsonResponse({'error':"POST request required.", "status": 400})




def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        profile = Profile(user=user)
        profile.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
