from django.shortcuts import render
import csv
import os
import pandas as pd
import geocoder as gc
import requests

# Create your views here.
def StatehousesIndexView(request):
    """View function for statehouses index page."""
    FILE_NAME = 'lobbyists-cloropleth-map.html'
    # If already generated, no need to do so again.
    DATA_PATH = os.path.abspath(os.path.dirname(__file__))
    FILE_PATH = DATA_PATH + '/static/statehouses/' + FILE_NAME

    try:
        os.stat(FILE_PATH)
    except:
        capitals = {
            'Alabama': 'Montgomery',
            'Alaska': 'Juneau',
            'Arizona':'Phoenix',
            'Arkansas':'Little Rock',
            'California': 'Sacramento',
            'Colorado':'Denver',
            'Connecticut':'Hartford',
            'Delaware':'Dover',
            'Florida': 'Tallahassee',
            'Georgia': 'Atlanta',
            'Hawaii': 'Honolulu',
            'Idaho': 'Boise',
            'Illinois': 'Springfield',
            'Indiana': 'Indianapolis',
            'Iowa': 'Des Moines',
            'Kansas': 'Topeka',
            'Kentucky': 'Frankfort',
            'Louisiana': 'Baton Rouge',
            'Maine': 'Augusta',
            'Maryland': 'Annapolis',
            'Massachusetts': 'Boston',
            'Michigan': 'Lansing',
            'Minnesota': 'St. Paul',
            'Mississippi': 'Jackson',
            'Missouri': 'Jefferson City',
            'Montana': 'Helena',
            'Nebraska': 'Lincoln',
            'Nevada': 'Carson City',
            'New Hampshire': 'Concord',
            'New Jersey': 'Trenton',
            'New Mexico': 'Santa Fe',
            'New York': 'Albany',
            'North Carolina': 'Raleigh',
            'North Dakota': 'Bismarck',
            'Ohio': 'Columbus',
            'Oklahoma': 'Oklahoma City',
            'Oregon': 'Salem',
            'Pennsylvania': 'Harrisburg',
            'Rhode Island': 'Providence',
            'South Carolina': 'Columbia',
            'South Dakota': 'Pierre',
            'Tennessee': 'Nashville',
            'Texas': 'Austin',
            'Utah': 'Salt Lake City',
            'Vermont': 'Montpelier',
            'Virginia': 'Richmond',
            'Washington': 'Olympia',
            'West Virginia': 'Charleston',
            'Wisconsin': 'Madison',
            'Wyoming': 'Cheyenne'
        } # create a dictionary, key is the state and value is the capital

        # Load replication data using IQSS dataverse client.
        from dataverse import Connection

        host = 'dataverse.unc.edu'                  # All clients >4.0 are supported
        token = '6d9aeda0-b118-4395-98e6-008646674b18'  # Generated at /account/apitoken

        # Grab data for https://dataverse.unc.edu/dataset.xhtml?persistentId=doi:10.15139/S3/3EAPI2
        try:
            connection = Connection(host, token)
            dataverse = connection.get_dataverse('UNC')
            dataset = dataverse.get_dataset_by_doi('DOI:10.15139/S3/3EAPI2')
            files = dataset.get_files('latest')
        except:
            import warnings
            warnings.warn('Problem with dataverse file pull.')
            # Check that geocoded csv doesn't already exist.
            try:
                filtered = read_csv(DATA_PATH + '/data/filtered.tsv', sep='\t')
            except:
                # Load replication data from file.
                df = pd.read_csv(DATA_PATH + '/data/Statehouses.tab.tsv', sep='\t')

                # Create a new dataframe with the columns we care about.
                filtered = df[['abbr', 'state', 'year', 'lobbyists']].copy()

                # Fill NaN as 0.aeau
                filtered.fillna(0, inplace=True)

                # Aggregate yearly data.
                # @See https://www.shanelynn.ie/summarising-aggregation-and-grouping-data-in-python-pandas/
                filtered = filtered.groupby(['abbr', 'state'])[['lobbyists']].sum().reset_index()

                # Load our geocoder.
                from geopy import geocoders
                gn = geocoders.GeoNames(username='kuranes')

                # Populate coordinate data.
                for index, row in filtered.iterrows():
                    # Get state capital.
                    try:
                        capital = capitals[row['state']]
                        g = gn.geocode(capital + ', ' + row['state'])
                        filtered.loc[index, 'lat'] = g.latitude
                        filtered.loc[index, 'lon'] = g.longitude
                    except:
                        import warnings
                        warnings.warn("no code found for " + capital + ', ' + row['state'])

        # TODO make sure we have a dataset here, if not throw exception.

        # Save geocoded data to csv.
        filtered.to_csv(DATA_PATH + '/data/filtered.tsv', sep='\t', encoding='utf-8')

        # Generate Choropleth using plotly.
        # @See https://plot.ly/python/configuration-options/#offline-configuration-options
        # @See https://plot.ly/python/choropleth-maps/#united-states-choropleth-map
        import plotly.plotly as py
        import plotly

        # Format numbers.
        filtered['lobbyists_formatted'] = filtered['lobbyists']
        filtered['lobbyists_formatted'] = filtered['lobbyists_formatted'].astype(float).apply(lambda x: "{:,.0f}".format(x))

        # Convert ints to strings.
        for col in filtered.columns:
            filtered[col] = filtered[col].astype(str)

        # TODO make a time series like https://github.com/plotly/dash-opioid-epidemic-demo/blob/master/app.py#L55
        # @See https://community.plot.ly/t/python-plotly-how-to-make-a-choropleth-map-with-a-slider-access-grid-data-issue/3218/8

        scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
                [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]

        data = [ dict(
                type='choropleth',
                colorscale = scl,
                autocolorscale = False,
                locations = filtered['abbr'],
                z = filtered['lobbyists'].astype(float),
                locationmode = 'USA-states',
                text = filtered['state'] + ': ' + filtered['lobbyists_formatted'] + ' total lobbyists',
                hoverinfo = 'text',
                marker = dict(
                    line = dict (
                        color = 'rgb(255,255,255)',
                        width = 2
                    ) ),
                colorbar = dict(
                    title = "Total State Lobbyists")
                ) ]

        layout = dict(
                title = 'Lobbyists Per State 1986-2013',
                geo = dict(
                    scope='usa',
                    projection=dict( type='albers usa' ),
                    showlakes = True,
                    lakecolor = 'rgb(255, 255, 255)'),
                     )

        fig = dict(data=data, layout=layout)
        html = plotly.offline.plot(fig, output_type='div')
        outfile = FILE_PATH

        with open(outfile, 'w') as f:
            f.write(html)

    context = {
        'filename': FILE_NAME
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'statehouses/statehouse_index.html', context)
