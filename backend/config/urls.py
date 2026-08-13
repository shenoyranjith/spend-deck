from django.urls import include, path, re_path

from core.views import frontend_index


urlpatterns = [
    path("api/", include("core.urls")),
    path("", frontend_index, name="frontend-index"),
    re_path(r"^(?!api/|static/).*$", frontend_index, name="frontend-route"),
]
