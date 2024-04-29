from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('accounts/login/', views.login_user , name="login_user"),
    path('accounts/register/', views.register, name="register"),
    path('accounts/logout/', views.logout_user, name="logout"),
    path('profile/', views.profile, name="profile"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('dashboard/comparative_analysis/', views.comparative_analysis, name="comparative_analysis"),
    path('dashboard/prereq_analysis/', views.prereq_analysis, name="prereq_analysis")

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)