from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from geoverse.apps.statehouses.views import StatehousesIndexView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
  path('', StatehousesIndexView, name='statehouses_index')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
