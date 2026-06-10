from django.urls import path
from . import views
#def _boom(request):                 # TEMPORARY
#    raise Exception("Test error")
urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.task_create, name='task_create'),
    path('<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),
    # Developer 2 : admin-only audit log
    path('audit-log/', views.audit_log, name='audit_log'),
    # Developer 2 : user profile page
    path('profile/', views.profile, name='profile'),
#    path('boom/', _boom),  
    path('search/', views.task_search, name='task_search'),
]

    