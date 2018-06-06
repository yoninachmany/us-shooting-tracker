utils
---

[geocode.py](https://github.com/yoninachmany/us-shooting-tracker/blob/master/utils/geocode.py) can be run simply with `python geocode.py`. It reads a local `Clean-articles-with-extracted-info.tsv` file (in the format outputted by [http://gun-violence.org](http://gun-violence.org/)) and uses spacy to extract all "location" entities from the article title and text. Then, each entity is geocoded using geocodio and google maps. The geocodio results are saved in a entity_to_geocodio python dictionary and the google maps results are saved in a entity_to_google python dictionary. These dictionaries are pickled and saved to disk. Each dictionary is a mapping from a string that occurs in an article to a geocoded (city, state).
