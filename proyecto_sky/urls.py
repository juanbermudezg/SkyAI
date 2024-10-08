"""
URL configuration for proyecto_sky project.

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
from django.urls import include, path
from sky import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', include('sky.urls', namespace='posts')),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', views.helloworld, name="home_page"),
    path('sign_up/', views.sign_up, name="sign_up"),
    path('sign_in/', views.sign_in, name="sign_in"),
    path('sign_out/', views.sign_out, name="sign_out"),
    path('flights/', views.flights, name="flights"),
    path('flight/<int:flight_id>/', views.flight_detail, name="flight_detail"),
    path('flight/<int:flight_id>/delete_flight/', views.delete_flight, name='delete_flight'),
    path('flights/create/', views.create_flight, name="create_flight"),
    path('profile/<int:profile_id>/', views.profile_detail, name="profile_detail"),
    path('profile/<int:profile_id>/delete_profile/', views.delete_profile, name='delete_profile'),
    path('profile/<int:profile_id>/update_profile/', views.update_profile, name='update_profile'),
    path('api/', include('sky.api.urls')),
]
