from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView

from core.models import Task


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stats"] = Task.objects.aggregate(
            total=Count("id"),
            completed=Count("id", filter=Q(is_completed=True)),
            pending=Count("id", filter=Q(is_completed=False)),
        )
        return context


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "core/task_list.html"
    context_object_name = "task_list"
    paginate_by = 5

    def get_queryset(self):
        return Task.objects.select_related("task_type").prefetch_related("assignees")


class MyTaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "core/my_task_list.html"
    context_object_name = "task_list"

    def get_queryset(self):
        return Task.objects.filter(assignees=self.request.user)


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = "core/task_detail.html"
    context_object_name = "task"


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    fields = [
        "name",
        "description",
        "deadline",
        "priority",
        "task_type",
        "assignees",
        "is_completed",
    ]
    success_url = reverse_lazy("core:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = [
        "name",
        "description",
        "deadline",
        "priority",
        "task_type",
        "assignees",
        "is_completed",
    ]
    template_name = "core/task_form.html"
    success_url = reverse_lazy("core:my-task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "core/task_confirm_delete.html"
    success_url = reverse_lazy("core:my-task-list")