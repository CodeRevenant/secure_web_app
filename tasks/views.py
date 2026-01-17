from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from auditlog.models import AuditLog

@login_required
def task_list(request):
    # --- TEMPORARY 500 ERROR TRIGGER FOR REPORT ---
    

    # RBAC implementation: Admins see all, Users see only their own
    if request.user.is_staff or request.user.groups.filter(name="Admin").exists():
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(owner=request.user)
    return render(request, "tasks/task_list.html", {"tasks": tasks})

@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid(): # 🔐 MANDATORY: Validate input to prevent Injection/XSS
            task = form.save(commit=False)
            task.owner = request.user
            task.save()

            # 🔐 AUDIT LOG — TASK CREATED
            AuditLog.objects.create(
                user=request.user,
                action=f"SECURE TASK CREATE: ID {task.id} - '{task.title}'",
                ip_address=request.META.get("REMOTE_ADDR")
            )
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "tasks/task_form.html", {"form": form})

@login_required
def task_delete(request, task_id):
    # Security Check: Ensure user owns the task or is an Admin
    if request.user.is_staff:
        task = get_object_or_404(Task, id=task_id)
    else:
        task = get_object_or_404(Task, id=task_id, owner=request.user)

    if request.method == "POST":
        # 🔐 AUDIT LOG — TASK DELETED
        AuditLog.objects.create(
            user=request.user,
            action=f"SECURE TASK DELETE: ID {task.id} - '{task.title}'",
            ip_address=request.META.get("REMOTE_ADDR")
        )
        task.delete()
        return redirect("task_list")
    
    return render(request, "tasks/task_confirm_delete.html", {"task": task})