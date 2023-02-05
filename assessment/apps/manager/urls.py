
from rest_framework.routers import SimpleRouter
from assessment.apps.manager.views import ProjectViewSet, TaskViewSet

projects_router = SimpleRouter()
projects_router.register("projects", ProjectViewSet)
tasks_router = SimpleRouter()
tasks_router.register("tasks", TaskViewSet)

