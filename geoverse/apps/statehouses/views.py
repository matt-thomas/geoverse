from django.shortcuts import render
import geoplotlib
import csv
import os

# Create your views here.
def StatehousesIndexView(request):
    """View function for statehouses index page."""

    # TODO load replication data.
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'data/Statehouses.tab.tsv')
    # df = read_csv(file_path, sep='\t')
    # import pdb
    # pdb.set_trace()
    # TODO geocode state house info.
    # TODO pass this info to geoplotlib.
    # TODO create visuals.
    # TODO pass image paths as context.

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'statehouses/statehouse_index.html')
