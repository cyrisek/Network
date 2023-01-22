import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import User, Profile, Post


def index(request):
    if request.user.is_authenticated:
        user = request.user
        posts = Post.objects.all().order_by('-timestamp')
        liked_posts = user.liked_posts.all()
        # Paginate the posts
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html", {
            "page_obj": page_obj,
            "user": user,
            "liked_posts": liked_posts,
        })
    else:
        posts = Post.objects.all().order_by('-timestamp')
        # Paginate the posts
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html", {
            "page_obj": page_obj,
        })


def jsons(request):
    # Easy way to look up Jsons
    data = list(Post.objects.values())
    profile = list(Profile.objects.values())
    return JsonResponse(profile, safe=False)


@ csrf_exempt
@ login_required
def like_post(request, id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    post = Post.objects.get(id=id)
    result = False

    user = request.user
    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
        result = False
    else:
        post.likes.add(user)
        result = True
    post.save()
    return JsonResponse({"liked": result, "count": post.likes.count()}, status=200)


@ csrf_exempt
@ login_required
def follow(request, id):
    if request.method == "POST":
        user = request.user
        profile_user = Profile.objects.get(id=id)
        if profile_user.followers.filter(id=user.id).exists():
            profile_user.followers.remove(user)
        else:
            profile_user.followers.add(user)
        return HttpResponseRedirect(reverse("profile", args=(profile_user, )))


@ csrf_exempt
@ login_required
def edit(request, id):
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400)
    post = Post.objects.get(id=id)
    body = post.body
    return JsonResponse({"body": body}, status=200)


@ csrf_exempt
@ login_required
def save(request, id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    post = Post.objects.get(id=id)
    post.body = data['body']
    body = post.body
    post.save()
    return JsonResponse({"body": body}, status=200)


def profiles(request, id):
    if request.user.is_authenticated:
        user = User.objects.get(username=id)
        user2 = request.user
        profile_user = Profile.objects.get(user=user)
        if profile_user.followers.filter(id=user2.id).exists():
            msg = False
        else:
            msg = True
        user_profile, created = Profile.objects.get_or_create(user=user)
        posts = Post.objects.filter(user=user).order_by('-timestamp')
        liked_posts = user2.liked_posts.all()
        paginator = Paginator(posts, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'network/profile.html', {
            "user": user,
            "profile": user_profile,
            "page_obj": page_obj,
            "liked_posts": liked_posts,
            "user2": user2,
            "msg": msg,
        })
    else:
        user = User.objects.get(username=id)
        profile_user = Profile.objects.get(user=user)
        user_profile, created = Profile.objects.get_or_create(user=user)
        posts = Post.objects.filter(user=user).order_by('-timestamp')
        paginator = Paginator(posts, 3)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'network/profile.html', {
            "user": user,
            "profile": user_profile,
            "page_obj": page_obj,
        })


@ login_required
def following(request):
    user = request.user
    profiles = Profile.objects.filter(followers=user)
    liked_posts = user.liked_posts.all()
    posts = []
    for profile in profiles:
        user_post = Post.objects.filter(
            user_id=profile.user_id).order_by('-timestamp')
        for post in user_post:
            posts.append(post)

    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "page_obj": page_obj,
        "liked_posts": liked_posts,
    })


@ csrf_exempt
@ login_required
def new_post(request):
    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check post
    data = json.loads(request.body)
    posts = [post.strip() for post in data.get("body").split(",")]
    if posts == [""]:
        return JsonResponse({
            "error": "At least post required."
        }, status=400)

    # Convert post to NewPost object
    post = data.get("body", "")
    post = Post(
        user=request.user,
        body=post,
    )
    post.save()
    return JsonResponse({"message": "Post saved successfully."}, status=201)


@ csrf_exempt
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


@ csrf_exempt
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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
