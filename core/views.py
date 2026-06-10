from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .models import Task, AuditLog
from .forms import TaskForm, RegistrationForm
from .decorators import admin_required


def _client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


# ============================================================
#  Developer 2 :  REGISTRATION
# ============================================================
def register(request):
    if request.user.is_authenticated:
        return redirect('task_list')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # password is hashed by UserCreationForm
            AuditLog.objects.create(
                username=user.username, action='register',
                ip_address=_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:255],
            )
            # New accounts are always normal users (profile created via signal)
            login(request, user)  # rotates the session key -> session fixation safe
            messages.success(request, 'Account created successfully. Welcome!')
            return redirect('task_list')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


# ============================================================
#  Developer 2 :  AUDIT LOG PAGE  (Admin only - RBAC enforced)
# ============================================================

#@login_required  # BEFORE: hanya semak login, tiada semakan peranan
@admin_required
def audit_log(request):
    logs = AuditLog.objects.all()[:200]  # newest 200 entries
    return render(request, 'core/audit_log.html', {'logs': logs})


# ============================================================
#  Developer 2 :  USER PROFILE PAGE  (Functional Requirement #4)
# ============================================================
@login_required
def profile(request):
    # Shows the logged-in user's own info only (no IDOR - always request.user)
    task_count = Task.objects.filter(owner=request.user).count()
    return render(request, 'core/profile.html', {
        'profile_user': request.user,
        'task_count': task_count,
    })


# ============================================================
#  Developer 1 :  Secure CRUD  (unchanged)
# ============================================================
@login_required
def task_list(request):
    tasks = Task.objects.filter(owner=request.user)
    return render(request, 'core/task_list.html', {'tasks': tasks})


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user  # prevent IDOR
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'core/task_form.html', {'form': form, 'action': 'Create'})


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)  # IDOR protection
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'core/task_form.html', {'form': form, 'action': 'Edit'})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)  # IDOR protection
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')
    return render(request, 'core/task_confirm_delete.html', {'task': task})

#@login_required
#def task_search(request):
#    q = request.GET.get('q', '')
#    # VULNERABLE: raw SQL + string concat (TEMPORARY - untuk demo before)
#    query = "SELECT * FROM core_task WHERE title LIKE '%" + q + "%'"
#    tasks = list(Task.objects.raw(query))
#   return render(request, 'core/task_list.html', {'tasks': tasks})

@login_required
def task_search(request):
    q = request.GET.get('q', '')
    tasks = Task.objects.filter(title__icontains=q, owner=request.user)
    return render(request, 'core/task_list.html', {'tasks': tasks})
