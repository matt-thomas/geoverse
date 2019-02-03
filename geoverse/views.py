from django.shortcuts import render

# Create your views here.
def LandingIndexView(request):
    """View function for index page."""

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'base_index.html')
