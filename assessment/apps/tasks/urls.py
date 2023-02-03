from rest_framework.routers import SimpleRouter
from assessment.apps.tasks.views import TaskViewSet




tasks_router = SimpleRouter()
tasks_router.register("tasks", TaskViewSet)
urlpatterns = tasks_router.urls

