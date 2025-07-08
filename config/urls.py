from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from mailing.views import base_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('mailing/', include('mailing.urls', namespace='mailing')),
    path('accounts/', include([
        path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login')])),
    path('', base_view, name='main'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
