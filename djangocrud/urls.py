"""djangocrud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from tasks import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.helloword),
    path('home/', views.helloword, name="home"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('analytics/', views.analytics, name="analytics"),
    path('data/', views.data, name="data"),
    path('logout/', views.signout, name="logout"),
    path('login/', views.signin, name="login"),
    path('create/', views.create, name="create"),
    path('improve/', views.improve, name="improve"),
    path('profile/', views.profile, name="profile"),
    path('download-data/', views.download_all_data, name='download-all-data'),

]
urlpatterns += staticfiles_urlpatterns()