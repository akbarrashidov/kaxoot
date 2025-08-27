from django.urls import path
from .views import RegisterView, LoginView, AdminGoogleView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("admin/google/", AdminGoogleView.as_view(), name="admin-google"),
]