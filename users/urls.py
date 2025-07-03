from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, edit_profile, email_verification, view_own_profile, view_profile

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', LogoutView.as_view(next_page='main'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/<int:pk>/', view_profile, name='profile'),
    path('profile/', view_own_profile, name='profile_own'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
