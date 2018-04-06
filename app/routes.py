from flask import render_template, Response
from app import app

import os
import datetime
import geojson
import io
import csv

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/download')
def download():
    """Download a csv file of all the data."""

    current_date = str(datetime.date.today())
    csv_name = 'data-dump-' + current_date + '.csv'

    cd = os.path.dirname(__file__)
    with open(os.path.join(cd, 'static/final-output.geojson')) as f:
        data = geojson.loads(f.read())

    short_to_long_name = {
        'coordinates': 'coordinates',
        'articleUrl': 'url',
        'articleTitle': 'title',
        'date': 'date',
        'time': 'time',
        'knewEachOther': 'The shooter and the victim knew each other',
        'domesticViolence': 'The incident was a case of domestic violence',
        'anotherCrime': 'The firearm was used during another crime',
        'selfDefense': 'The firearm was used in self defense',
        'alcohol': 'Alcohol was involved',
        'drugs': 'Drugs (other than alcohol) were involved',
        'selfDirected': 'The shooting was self-directed',
        'suicideOrAttempt': 'The shooting was a suicide or suicide attempt',
        'unintentional': 'The shooting was unintentional',
        'byOfficer': 'The shooting was by a police officer',
        'atOfficer': 'The shooting was directed at a police officer',
        'stolen': 'The firearm was stolen',
        'familyOwned': 'The firearm was owned by the victim/victims family'
    }

    fieldnames = ['coordinates', 'url', 'title', 'date', 'time',
                  'The shooter and the victim knew each other',
                  'The incident was a case of domestic violence',
                  'The firearm was used during another crime',
                  'The firearm was used in self defense',
                  'Alcohol was involved',
                  'Drugs (other than alcohol) were involved',
                  'The shooting was self-directed',
                  'The shooting was a suicide or suicide attempt',
                  'The shooting was unintentional',
                  'The shooting was by a police officer',
                  'The shooting was directed at a police officer',
                  'The firearm was stolen',
                  'The firearm was owned by the victim/victims family']

    output = io.StringIO()
    wr = csv.DictWriter(output, fieldnames=fieldnames)
    wr.writeheader()

    for feature in data.features:
        row = {}
        row['coordinates'] = str(feature.geometry.coordinates)

        for key, value in feature.properties.items():
            row[short_to_long_name[key]] = value

        wr.writerow(row)

    return Response(output.getvalue(), mimetype='text/csv', headers={'Content-disposition': 'attachment; filename={}'.format(csv_name)})