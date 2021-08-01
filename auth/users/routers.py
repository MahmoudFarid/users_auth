from rest_framework.routers import SimpleRouter

from auth.users.views import UserViewSet

app_name = "users"

router = SimpleRouter()

router.register("", UserViewSet)

urlpatterns = router.urls
