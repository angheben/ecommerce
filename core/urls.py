from django.contrib.auth import views as auth_views
from django.urls import path
from .views import IndexView, FormsView
from .forms import SignupForm, LoginForm

app_name = 'core'

urlpatterns = [
    path("", IndexView.as_view(), name='index'),
    path("signup/", FormsView.as_view(form_class=SignupForm), name='signup'),
    path("login/", auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm),
         name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
