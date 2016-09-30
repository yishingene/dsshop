"""dsshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url, include, patterns
from django.conf import settings
from django.contrib import admin
from oscar.app import application

from oscarapi.app import application as api

from other_pages import views as other_views


urlpatterns = [

	url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^admin/', admin.site.urls),

    url(r'^contact/$', other_views.ContactPageView.as_view(), name='contact'),

    url(r'', include(application.urls)),

    url(r'^api/', include(api.urls)),
]

urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
