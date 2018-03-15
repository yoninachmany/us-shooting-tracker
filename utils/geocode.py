import pandas as pd
import googlemaps
from geocodio import GeocodioClient
from geocodio.exceptions import GeocodioDataError
import spacy
from spacy import displacy

import collections
import time
import pickle

# BEGIN UTILITIES

us_state_abbrev = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming',
    'PR': 'Puerto Rico',
    'DC': 'District of Columbia'
}

geo_client = GeocodioClient('304731ec51c50c0a50fa3361aec076167e106a0')
gmaps = googlemaps.Client(key='AIzaSyCTZcOWn00WeFoSSRcjwbATgGF6epsHIOs')


def get_city_state_google(location):
    """
    location: str
    :returns [(city, state)]
    """
    ret = []

    try:
        geocode_result = gmaps.geocode(location, components={'country': 'US'})
    except googlemaps.exceptions.HTTPError:
        return ret

    for result in geocode_result:
        result_state = None
        result_city = None

        for component in result['address_components']:
            if 'locality' in component['types']:
                result_city = component['long_name']

            elif 'administrative_area_level_1' in component['types']:
                result_state = component['long_name']

        if result_state is not None or result_city is not None:
            ret.append((result_city, result_state))

    return ret


def get_city_state_geocodio(location):
    """
    location: str
    :returns [(city, state)]
    """
    ret = []

    try:
        geocode_result = geo_client.geocode(location)
    except GeocodioDataError:
        return ret

    for result in geocode_result['results']:
        result_state = None
        result_city = None

        if 'city' in result['address_components']:
            result_city = result['address_components']['city']

        if 'state' in result['address_components']:
            result_state = us_state_abbrev[result['address_components']['state']]

        if result_state is not None or result_city is not None:
            ret.append((result_city, result_state))

    return ret

# END UTILITIES

nlp = spacy.load('en')

article_df = pd.read_csv('Clean-articles-with-extracted-info.tsv', sep='\t')

# entity_to_google is a mapping from entity (e.g. 'Ferguson') to a list of
# (city, state) tuples.
# entity_to_google = {}

# entity_to_geocodio is a mapping from entity (e.g. 'Ferguson') to a list of
# (city, state) tuples.
entity_to_geocodio = pickle.load(open('entity_to_geocodio.p', 'rb'))

locs_seen_already = set(entity_to_geocodio.keys())

t0 = time.time()

for i in range(len(article_df)):
    if i % 100 == 0:
        # pickle.dump(entity_to_google, open('entity_to_google.p', 'wb'))
        pickle.dump(entity_to_geocodio, open('entity_to_geocodio.p', 'wb'))
        print('{} way done, {} entities so far, i is {}, taken {} seconds'.format(i / len(article_df), len(locs_seen_already), i, time.time() - t0))

    doc_ex = nlp(article_df['Article title'].iloc[i] + '. ' + article_df['Full text'].iloc[i])

    locs = []

    org_loc_keywords = ['JAIL', 'PRISON', 'POLICE', 'MEDICAL', 'HOSPITAL', 'PARK']

    # Store relevant entity labels
    for e in doc_ex.ents:
        if e.label_ == 'GPE':
            locs.append(e.text)
        elif e.label_ == 'LOC':
            locs.append(e.text)
        elif e.label_ == 'ORG' and any(keyword in e.text.upper() for keyword in org_loc_keywords):
            locs.append(e.text)
        elif e.label_ == 'FAC':
            locs.append(e.text)

    for loc in locs:
        if loc not in locs_seen_already:
            # try:
            #     entity_to_google[loc] = get_city_state_google(loc)
            # except Exception as e:
            #     print('exception in get_city_state_google on {}: {}'.format(loc, e))

            try:
                entity_to_geocodio[loc] = get_city_state_geocodio(loc)
            except Exception as e:
                print('exception in get_city_state_geocodio on {}: {}'.format(loc, e))

            locs_seen_already.add(loc)

t1 = time.time()

print('took {} seconds'.format(t1 - t0))
print('there are {} entities'.format(len(locs_seen_already)))

# TODO: Note that geocodio returns lots more results than google, especially
# on ambiguous results. This could be a problem, handle later!

# pickle.dump(entity_to_google, open('entity_to_google.p', 'wb'))
pickle.dump(entity_to_geocodio, open('entity_to_geocodio.p', 'wb'))
