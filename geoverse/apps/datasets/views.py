from django.shortcuts import render

# Create your views here.
def DatasetsIndexView(request):
    """View function for datasets index page."""

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'datasets/dataset_index.html')
