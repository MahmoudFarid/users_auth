from django.urls import include, path

app_name = "api"

urlpatterns = [
    path("users/", include("auth.users.routers", namespace="rest_users")),
]
