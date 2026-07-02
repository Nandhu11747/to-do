from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm


def home(request):

    tasks = Task.objects.all()

    return render(request, "todo/home.html", {"tasks": tasks})


def add_task(request):

    if request.method == "POST":

        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("home")

    else:

        form = TaskForm()

    return render(request, "todo/add_task.html", {"form": form})


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


def delete_task(request, id):
    task = Task.objects.get(id=id)
    task.delete()
    return redirect("home")


def complete_task(request, id):
    task = Task.objects.get(id=id)
    task.completed = not task.completed
    task.save()
    return redirect("home")