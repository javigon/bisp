from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from django.conf.urls.defaults import *
from tastypie.api import Api
from userapi.api import *
from repo.models import *

from django.contrib import admin
admin.autodiscover()
admin.site.register(Building)
admin.site.register(Measurement)

user_api = Api(api_name = 'user')
user_api.register(BuildingDataResource())
user_api.register(BuildingResource())
user_api.register(MeasurementsResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'engine.views.home', name='home'),
    # url(r'^engine/', include('engine.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Building representation
    (r'^api/', include(user_api.urls)),
)
