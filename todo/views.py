from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q 
from .models import Task
from .forms import TaskForm

@login_required
def task_list(request):
    query = request.GET.get('q') 
    status = request.GET.get('status') 
    due_date = request.GET.get('due_date') 

    tasks = Task.objects.filter(user=request.user) 

    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))

    if status:
        if status == 'completed':
            tasks = tasks.filter(is_completed=True)
        elif status == 'not_completed':
            tasks = tasks.filter(is_completed=False)

    if due_date:
        tasks = tasks.filter(due_date=due_date)

    context = {
        'tasks': tasks,
        'query': query,
        'status': status,      
        'due_date': due_date   
    }
    return render(request, 'todo/task_list.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Ҳисоби шумо "{username}" бомуваффақият сохта шуд! Акнун метавонед ворид шавед.')
            return redirect('login') 
    else:
        form = UserRegisterForm()
    return render(request, 'todo/register.html', {'form': form})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'todo/task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'todo/task_confirm_delete.html', {'task': task})
