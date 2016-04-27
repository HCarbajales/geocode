# geocode
A Python wrapper for various mapping APIs available on the web, including Google, Bing, MapQuest, ESRI, and Geocodio. Functions include geocoding and reverse-geocoding, routing or directions, and batch geocoding or distance matrix, with responses returned as parsed JSON objects or (x, y) tuples.

    Example usage:

    >>> import geocode
    >>> geo = geocode.Geotool()
    >>> response_google = geo.geocode_google('United States Capitol')
    >>> response_bing = geo.geocode_bing('Lincoln Memorial, DC')
    >>> response_mapquest = geo.geocode_mapquest('10 Elm St, Danvers, MA 01923')
    >>> response_geocodio = geo.geocode_geocodio('35 Oak Drive, Gray, ME 04039')
    >>> response_esri = geo.geocode_esri('Monticello in Charlottesville, VA')

*Don't know how to enable pip-installing a package right now. Just stick the 'geocode' folder in your `C:\Python27\ArcGIS10.3\Lib\site-packages` folder for now and `import geocode`. I suck, I know... sorry. ;) - John

To use pip install, do the following steps:
1) Open Command Prompt
2) type "python -m pip install geocoder", assuming you never touched the envoironment variable setting. If you do not know what I mean, then you should be fine.

To test process:
1) Open Command Prompt
2) type "python", python should open up
3) type "help("geocoder")", you should see stuff about the module appear. 
- Henry
