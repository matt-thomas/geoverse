from django.conf.urls import url, include
from django.urls import path
from geoverse.apps.datasets.views import DatasetsIndexView

urlpatterns = [
  path('', DatasetsIndexView, name='dataset_index')
]
