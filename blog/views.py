from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def home(request):
    all_posts = Post.objects.all().order_by('-id')

    my_posts = None
    if request.user.is_authenticated:
        my_posts = Post.objects.filter(author=request.user).order_by('-id')

    return render(request, 'index.html', {
        'all_posts': all_posts,
        'my_posts': my_posts
    })

@login_required
def create_post(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        Post.objects.create(
            title=title,
            content=content,
            author=request.user   # 🔥 important
        )

        return redirect("/")

    return render(request, "create.html")

@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)

    if post.author != request.user:
        return redirect("/")  # block access

    if request.method == "POST":
        post.title = request.POST.get("title")
        post.content = request.POST.get("content")
        post.save()
        return redirect("/")

    return render(request, "edit.html", {"post": post})

@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)

    if post.author != request.user and not request.user.is_staff:
        return redirect("/")   # block

    post.delete()
    return redirect("/")

def user_login(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            next_url = request.GET.get('next')
            return redirect(next_url if next_url else "/")
        else:
            error = "Invalid username or password"

    return render(request, "login.html", {"error": error})


def user_logout(request):
    logout(request)
    return redirect("/")

def signup(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            error = "Username already exists"
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect("/")

    return render(request, "signup.html", {"error": error})