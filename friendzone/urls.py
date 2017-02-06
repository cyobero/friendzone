"""friendzone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from views import *


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name='home'),
    url(r'^register/$', register, name='register'),
    url(r'^login/$', signin, name='login'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^about/$', about, name='about'),
    url(r'^(?P<username>\w+)/$', profile_page, name='profile_page'),
    url(r'^profile/edit/$', edit_profile, name='edit_profile'),
    url(r'^profile/edit/success/$', edit_profile_success, name='edit_profile_success'),
    url(r'^post/(\d+)/$', post, name='post'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
