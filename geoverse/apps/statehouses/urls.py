from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from geoverse.apps.statehouses.views import StatehousesIndexView

urlpatterns = [
  path('', StatehousesIndexView, name='statehouses_index')
]
