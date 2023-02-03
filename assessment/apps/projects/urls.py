
from rest_framework.routers import SimpleRouter
from assessment.apps.projects.views import ProjectViewSet




projects_router = SimpleRouter()
projects_router.register("projects", ProjectViewSet)
urlpatterns = projects_router.urls



