from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import Position, TaskType, Task, Worker


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "task_type",
        "priority",
        "deadline",
        "is_completed",
    )
    list_filter = ("task_type", "priority", "is_completed")
    search_fields = ("name", "description")
    filter_horizontal = ("assignees",)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("position",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info", {"fields": ("position",)}),
    )
    list_display = UserAdmin.list_display + ("position",)
