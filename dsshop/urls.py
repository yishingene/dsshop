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
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

from oscar.app import application
from oscar.apps.search import facets
from oscar.core.loading import get_class

from oscarapi.app import application as api

from other_pages import views as other_views


urlpatterns = [

	url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^nl/$', RedirectView.as_view(url='/', permanent=True)), 
    url(r'^fr/$', RedirectView.as_view(url='/', permanent=True)), 
    url(r'^en/$', RedirectView.as_view(url='/', permanent=True)), 

    url(r'^admin/', admin.site.urls),

    url(r'^contact/$', other_views.ContactPageView.as_view(), name='contact'),

    url(r'^send_shipping_charges_mail/(?P<order_id>\d+)/$', other_views.ShippingChargesMailView.as_view(), name='shipping-charges-mail'),
    url(r'^dashboard/events/$', other_views.EventListView.as_view(), name='event-list'),
    url(r'^dashboard/events/update/(?P<pk>\d+)/$', other_views.EventUpdateView.as_view(), name='event-update'),
    url(r'^dashboard/events/delete/(?P<pk>\d+)/$', other_views.EventDeleteView.as_view(), name='event-delete'),
    url(r'^upload/$', other_views.UploadView.as_view(), name='upload'),

    url(r'', include(application.urls)),

    url(r'^api/', include(api.urls)),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

