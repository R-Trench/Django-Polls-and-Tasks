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
            if len(request.POST['password1']) <9:
                return render(request, 'tasks/signupuser.html', {'form':UserCreationForm(), 'error':'password too short'})

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
    # ensures we only show the form if the page view isn't a submission
    if request.method  == 'GET':
        #renders template possing in dictionary maping {% ... form ...%} to the form above
        return render(request, 'tasks/createtodo.html', {'form':TodoForm()})
    else:
        #attempts to POST if input is valid
        try:
            form = TodoForm(request.POST)
            #tells us NOT to save it until we attach it to the proper user
            new_todo = form.save(commit=False)
            #attaches to logged in user
            new_todo.user = request.user
            new_todo.save()
            return redirect('tasks:currenttodos')
        except ValueError:
            #returns us to the same page with error message in the {{ error }} field of our template
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
