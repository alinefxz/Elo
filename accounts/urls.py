from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import RedirectView

from . import views
from .forms import LoginUsuarioForm


app_name = "accounts"

urlpatterns = [
    # Redireciona a página inicial para o login.
    path(
        "",
        RedirectView.as_view(
            pattern_name="accounts:login",
            permanent=False,
        ),
        name="inicio",
    ),

    path("cadastro/", views.cadastro, name="cadastro"),

    path(
        "login/",
        LoginView.as_view(
            template_name="accounts/login.html",
            authentication_form=LoginUsuarioForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),

    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard",
    ),
]