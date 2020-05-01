from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

def homepage(request):
    return render(request, 'tasks/homepage.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'tasks/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:

            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks:currenttodos')

            except IntegrityError:
                return render(request, 'tasks/signupuser.html', {'form':UserCreationForm(), 'error':'Username taken'})

        else:
            return render(request, 'tasks/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'tasks/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'tasks/loginuser.html', {'form':AuthenticationForm(), 'error':'Username/password did not match'})
        else:
            login(request, user)
            return(redirect('tasks:currenttodos'))

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('tasks:homepage')

@login_required
def createtodo(request):
    if request.method  == 'GET':
        return render(request, 'tasks/createtodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('tasks:currenttodos')
        except ValueError:
            return render(request, 'tasks/createtodo.html', {'form':TodoForm(), 'error':'invalid input'})

@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=True).order_by('created')
    return render(request, 'tasks/currenttodos.html', {'todos':todos})

@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')
    return render(request, 'tasks/completedtodos.html', {'todos':todos})

@login_required
def viewtodos(request, todo_pk):
    #loads in todo database - user=request.user ensures users only see items they created
    todo = get_object_or_404(Todo, pk=todo_pk, user = request.user)

    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'tasks/viewtodos.html', {'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('tasks:currenttodos')
        except ValueError:
            return render(request, 'tasks/viewtodos.html', {'todo':todo, 'form':form, 'error':'input not accepted'})

@login_required
def completetodos(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.date_completed = timezone.now()
        todo.save()
        return redirect('tasks:currenttodos')

@login_required
def deletetodos(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == "POST":
        todo.delete()
        return redirect('tasks:currenttodos')
