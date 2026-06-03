from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('core.urls')),

    # Developer 2 : Registration + Login/Logout
    path('accounts/register/', core_views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),

    # send the site root to the task list (login_required handles auth)
    path('', RedirectView.as_view(url='/tasks/', permanent=False)),
]
