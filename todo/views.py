from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm

@login_required
def home(request):

    tasks = Task.objects.all()

    return render(request, "todo/home.html", {"tasks": tasks})

@login_required
def add_task(request):

    if request.method == "POST":

        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("home")

    else:

        form = TaskForm()

    return render(request, "todo/add_task.html", {"form": form})

@login_required
def edit_task(request, task_id):

    task = Task.objects.get(id=task_id)

    if request.method == "POST":

        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect("home")

    else:

        form = TaskForm(instance=task)

    return render(request, "todo/edit_task.html", {"form": form})

@login_required
def delete_task(request, id):
    task = Task.objects.get(id=id)
    task.delete()
    return redirect("home")

@login_required
def complete_task(request, id):
    task = Task.objects.get(id=id)
    task.completed = not task.completed
    task.save()
    return redirect("home")


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "todo/signup.html", {
                "error": "Username already exists."
            })
        
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("login")
    
    return render(request, "todo/signup.html")


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")
        
        return render(request,"todo/login.html", {
            "error": "Invalid username or password."
        })
    
    return render(request, "todo/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")