from django.urls import path
from .views import RegisterView, LoginView, AdminGoogleView,ProfileUpdateView, ChangePasswordView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("admin/google/", AdminGoogleView.as_view(), name="admin-google"),
    path("profile/update/", ProfileUpdateView.as_view(), name="profile-update"),
    path("profile/change-password/", ChangePasswordView.as_view(), name="change-password"),
]
