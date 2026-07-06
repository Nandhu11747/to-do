from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Task
from .forms import TaskForm

@login_required
def home(request):

    if request.user.is_superuser:
        tasks = Task.objects.filter(
            created_by=request.user
        ).order_by("-created_at")
    else:
        tasks = Task.objects.filter(
            assigned_to=request.user
        ).order_by("-created_at")

    context = {
        "tasks": tasks,
        "total_tasks": tasks.count(),
        "completed_tasks": tasks.filter(completed=True).count(),
        "pending_tasks": tasks.filter(completed=False).count(),
    }

    return render(request, "todo/home.html", context)


@login_required
def add_task(request):

    if request.method == "POST":
        form = TaskForm(request.POST)
    else:
        form = TaskForm()

    if not request.user.is_superuser:
        form.fields.pop("assigned_to", None)

    if request.method == "POST" and form.is_valid():

        task = form.save(commit=False)
        task.created_by = request.user

        if not request.user.is_superuser:
            task.assigned_to = request.user

        task.save()
        return redirect("home")

    return render(request, "todo/add_task.html", {
        "form": form
    })


@login_required
def edit_task(request, task_id):

    if request.user.is_superuser:
        task = get_object_or_404(Task, id=task_id)
    else:
        task = get_object_or_404(
            Task, 
            id=task_id, 
            assigned_to=request.user)

    if request.method == "POST":

        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect("home")

    else:

        form = TaskForm(instance=task)

    return render(request, "todo/edit_task.html", {"form": form})

@login_required
def delete_task(request,task_id):
    
    if request.user.is_superuser:
        task = get_object_or_404(Task, id=task_id)
    else:
        task = get_object_or_404(
            Task, 
            id=task_id, 
            assigned_to=request.user
        )
    
        if task.created_by != request.user:
            return redirect("home")
        

    task.delete()
    return redirect("home")

@login_required
def complete_task(request, task_id):
    
    if request.user.is_superuser:
        task = get_object_or_404(Task, id=task_id)
    else:
        task = get_object_or_404(
            Task, 
            id=task_id, 
            assigned_to=request.user)


    task.completed = not task.completed
    task.save()
    return redirect("home")


def signup(request):
    if request.method == "POST":
        
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "todo/signup.html", {
                "error": "Passwords do not match."
            })

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