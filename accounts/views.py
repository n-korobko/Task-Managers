from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import redirect

from .forms import WorkerRegistrationForm


class RegisterView(CreateView):
    form_class = WorkerRegistrationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("core:task-list")
        return super().dispatch(request, *args, **kwargs)
