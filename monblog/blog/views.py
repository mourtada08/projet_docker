from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Task
from .forms import TaskForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse

@login_required
def update_task_status(request, task_id, new_status):
    task = Task.objects.get(id=task_id)
    task.statut = new_status
    task.save()
    return JsonResponse({"success": True})

@login_required
def task_list(request):
    query = request.GET.get('q')
    if request.user.is_superuser:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(assigned_to=request.user)
    
    if query:
        tasks = tasks.filter(titre__icontains=query)
    
    return render(request, 'blog/task_list.html', {'tasks': tasks})
@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            if task.assigned_to and task.assigned_to.email:
                send_mail(
                    'Nouvelle tâche assignée',
                    f'Bonjour {task.assigned_to.username}, une tâche vous a été assignée : {task.titre}',
                    'noreply@monblog.local',
                    [task.assigned_to.email],
                )
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'blog/task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'blog/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, created_by=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'blog/task_confirm_delete.html', {'task': task})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('task_list')  
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def mark_task_done(request, task_id):
    task = Task.objects.get(id=task_id)
    task.statut = "DONE"
    task.save()
    return JsonResponse({"success": True})


