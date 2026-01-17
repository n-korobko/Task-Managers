from django.urls import path
from core import views
from core.views import IndexView

app_name = "core"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("tasks/", views.TaskListView.as_view(), name="task-list"),
    path("tasks/my/", views.MyTaskListView.as_view(), name="my-task-list"),
    path("tasks/create/", views.TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/", views.TaskDetailView.as_view(), name="task-detail"),
    path(
        "tasks/<int:pk>/update/",
        views.TaskUpdateView.as_view(),
        name="task-update",
    ),
    path(
        "tasks/<int:pk>/delete/",
        views.TaskDeleteView.as_view(),
        name="task-delete",
    ),
]