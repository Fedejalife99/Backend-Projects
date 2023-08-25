"""
URL configuration for Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from app.views import new_reservation, new_place, home, register, sign_in, all_hotel, my_hotels, sign_out, profile, my_reservations, delete_res
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', home, name="home"),
    path('user/reservation', new_reservation, name="newres"),
    path('', sign_in, name="login"),
    path('register', register, name="register"),
    path('addplace', new_place, name="newplace"),
    path('homes', all_hotel, name="hotel"),
    path('myhotels', my_hotels, name="my_hotels"),
    path('logout', sign_out, name="logout"),
    path('profile', profile, name="profile"),
    path('user/res', my_reservations, name="myres"),
    path('res/del', delete_res, name='delres')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
