from django.urls import path, include
from rest_framework.routers import SimpleRouter
from assessment.apps.manager.views import ProjectViewSet, TaskViewSet


projects_router = SimpleRouter()
tasks_router = SimpleRouter()

projects_router.register("projects", ProjectViewSet)
tasks_router.register("tasks", TaskViewSet)


urlpatterns = [
    path('', include(projects_router.urls)),
    path('', include(tasks_router.urls)),
]
