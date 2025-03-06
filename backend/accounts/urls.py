from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from django.urls import path, include
from .views import GoogleLogin, UserDetailView


app_name = "accounts"

urlpatterns = [
    path("google/auth/", GoogleLogin.as_view(), name="google_login"),
    path("register/", RegisterView.as_view(), name="rest_register"),
    path("login/", LoginView.as_view(), name="rest_login"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path("user/", UserDetailsView.as_view(), name="rest_user_details"),
    path("user-detail/", UserDetailView.as_view(), name="user-detail"),
]
