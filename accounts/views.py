from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import WorkerRegistrationForm

def register(request):
    if request.user.is_authenticated:
        return redirect("core:task-list")

    if request.method == 'POST':
        form = WorkerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("core:task-list")
    else:
        form = WorkerRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})
