"""recipe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index),
    path('signin/',signin),
    path('signup/',signup),
    path("main/",main),
    path("findrecep/",findrecep),
    path("signout/" , signout),
    path("findcuisine/<int:number>/",findcuisine),
    path("reclist/<str:pred>/", reclist),
    path("addrecep/", addrecep),
    path("adding_recep/<int:number>/",adding_recep),
    path("profile/", profile),
    path("search/",search)

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
