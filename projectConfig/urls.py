"""
URL configuration for projectConfig project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from projects import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('projects/<str:tag>/', views.ProjectsView.as_view(), name='projects'),
    path('single-project/<uuid:key>/', views.ViewProjectView.as_view(), name='single_project'),
    # path('login/', views.LoginView.as_view(), name='login'),
    # path('logout/', views.LogoutView.as_view(), name='logout'),
    # path('add-project/', views.AddProjectView.as_view(), name='add_project'),
    # path('all-projects/', views.AllProjectsView.as_view(), name='all_projects'),
    # path('edit-project/<uuid:key>/', views.EditProjectView.as_view(), name='edit_project'),
    # path('add-image/<uuid:key>/', views.AddImageView.as_view(), name='add_image'),
    # path('delete-image/<int:pk>/', views.DeleteImageView.as_view(), name='delete_image'),
    # path('delete-project/<uuid:key>/', views.DeleteProjectView.as_view(), name='delete_project'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'projects.views.page404'
handler500 = 'projects.views.page500'
