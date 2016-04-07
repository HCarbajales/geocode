#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "John K. Tran"
__contact__ = "johtran@deloitte.com"

#------------------------------------------------------------------------------#
# Name:        Geotool.py                                                      #
# Created:     04/01/2016 08:14:19                                             #
# Version:     1.0                                                             #
#                                                                              #
# Purpose:     A Python wrapper for various mapping APIs available on the web, #
#              including Google, Bing, MapQuest, ESRI, and Geocodio. Functions #
#              include geocoding and reverse-geocoding, routing or directions, #
#              and batch geocoding or distance matrix, with responses returned #
#              as parsed JSON objects or (x, y) tuples.                        #
#                                                                              #
#------------------------------------------------------------------------------#


from pprint import pprint
import urllib
import json

try: import googlemaps
except ImportError: print 'ALERT: No googlemaps library found. Download "goo'\
       'glemaps" at (https://github.com/googlemaps/google-maps-services-python'\
       ') or "pip install googlemaps".'


class Geotool(object):
    """A geo utilities class contain standard API functionality (geocoding,
    routing) from major map API vendors - Bing Maps, Geocodio, Google Maps, ESRI
    and MapQuest.

    Example usage:

    >>> import geocode
    >>> geo = geocode.Geotool()
    >>> response_google = geo.geocode_google('United States Capitol')
    >>> response_bing = geo.geocode_bing('Lincoln Memorial, DC')
    >>> response_mapquest = geo.geocode_mapquest('10 Elm St, Danvers, MA 01923')
    >>> response_geocodio = geo.geocode_geocodio('35 Oak Drive, Gray, ME 04039')
    >>> response_esri = geo.geocode_esri('Monticello in Charlottesville, VA')
    """
    # John's Account Keys as class attributes
    _bing_maps_key = 'Au3e1tS1AZHWUG4qSGbUWCFboB-BZW5YC0pHtZTYXGZvLIJ-'\
        '6SrkwkFUZ2JZ4Pzk'
    _mapquest_consumer_key = 'JmkWyv9UabApfG3aCYWtQggY7fB03Fpr'
    _mapquest_consumer_secret = 'UrDy9QlQHI8s02Qk'
    _google_maps_browser_key = 'AIzaSyCLlnuKNkTw0oKlwUSO6fdXnL1RTs28_rw'
    _google_maps_server_key = 'AIzaSyDIWatA967gBKF5sNGhGydb0XY-ExBKdkY'
    _geocodio_app_key = '000ff728aa2fd8ae7737572b0afa5ef50d05dae'

    def __init__(self):
        """A geo utilities class contain standard API functionality (geocoding,
        routing) from major map API vendors - Bing Maps, Geocodio, Google Maps, ESRI
        and MapQuest.

        Example usage:

        >>> import geocode
        >>> geo = geocode.Geotool()
        >>> resp_google = g.geocode_google('United States Capitol')
        >>> resp_bing = g.geocode_bing('Lincoln Memorial, DC')
        >>> resp_mapquest = g.geocode_mapquest('10 Elm St, Danvers, MA 01923')
        >>> resp_geocodio = g.geocode_geocodio('35 Oak Drive, Gray, ME 04039')
        >>> resp_esri = g.geocode_esri('Monticello in Charlottesville, VA')
        """
        pass

    def geocode_esri(self, address, output='json', return_coords_only=False):
        """ The 'find' operation geocodes one location per request; the input
        address is specified in a single parameter. The find operation supports
        finding the following types of locations: street addresses, points of
        interest, administrative place names, postal codes, and (x, y)
        coordinates.

        References:
        developers.arcgis.com/rest/geocode/api-reference/geocoding-find.htm

        Params:
        {address}: an address or place name, e.g. 'US Capitol' *required
        {output}: the output type - 'json' or 'pjson'
        {return_coords_only}: return only (x, y) i.e. (LON, LAT) tuple - Boolean

        Raw URL Example:
        http://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/find?
        text=380%20New%20York%20Street%2C%20Redlands%2C%20CA%2092373&f=json

        Usage Limits:
        None

        Response:
        Return single best-match location.
        """
        query = 'http://geocode.arcgis.com/arcgis/rest/services/World/GeocodeS'\
            'erver/find?text={addr}&f={out}&outFields=*'.format(
                addr=urllib.quote(address),
                out=output.lower())
        response = urllib.urlopen(query)
        data_string = ''
        for line in response:
            data_string += line
        data_parsed = json.loads(data_string)
        if return_coords_only:
            try:
                x = data_parsed['locations'][0]['feature']['geometry']['x']
                y = data_parsed['locations'][0]['feature']['geometry']['y']
                return (x, y)
            except:
                pprint("WARNING: Couldn't find the (x, y) coordinates.")
                return (0.0, 0.0)
        else:
            return data_parsed

    def geocode_bing(self, address, output='json', return_coords_only=False,
        bing_key=_bing_maps_key):
        """Geocodes a 'query string' using the Locations API in Microsoft Bing
        Maps engine (https://msdn.microsoft.com/en-us/library/ff701711.aspx).
        The query is an address or place name. For instance, 'Space Needle' (a
        landmark) and '1 Microsoft Way, Redmond, WA 98052' (an address) are
        examples of query strings that can be geocoded. Output options are
        'json' (default) and 'xml'.

        References:
        https://msdn.microsoft.com/en-us/library/ff701711.aspx

        Params:
        {address}: an address or place name, e.g. 'US Capitol' *required
        {output}: the output type - 'json' or 'xml'
        {return_coords_only}: return only (x, y) i.e. (LON, LAT) tuple - Boolean
        {bing_key}: a custom Bing Maps Key; default is John's key - string

        Raw URL Example:
        http://dev.virtualearth.net/REST/v1/Locations?query=1%20Microsoft%20Way%
        20Redmond%20WA%2098052&output=json&key=BingMapsKey

        Usage Limits:
        50,000 transactions per day
        125,000 transactions per year

        Response:
        Returns multiple possible locations.
        """
        query = 'http://dev.virtualearth.net/REST/v1/Locations?'\
            'query={addr}&output={out}&key={bkey}'.format(
                bkey=bing_key,
                addr=urllib.quote(address),
                out=output.lower())
        response = urllib.urlopen(query)
        data_string = ''
        for line in response:
            data_string += line
        data_parsed = json.loads(data_string)
        if return_coords_only:
            if len(data_parsed['resourceSets'][0]['resources']) == 0:
                pprint("WARNING: Couldn't find the (x, y) coordinates.")
                return (0.0, 0.0)
            elif len(data_parsed['resourceSets'][0]['resources']) == 1:
                lat, lon = data_parsed['resourceSets'][0]['resources'][0]\
                    ['point']['coordinates']
                return (lon, lat)
            else:
                coords_list = []
                for resource in data_parsed['resourceSets'][0]['resources']:
                    lat, lon = resource['point']['coordinates']
                    coords_list.append((lon, lat))
                return coords_list
        else:
            return data_parsed

    def geocode_mapquest(self, address, output='json', return_coords_only=False,
        mapquest_key=_mapquest_consumer_key):
        """The geocoding service enables you to take an address and get the
        associated latitude and longitude. You can also use any latitude and
        longitude pair and get the associated address. Three types of geocoding
        are offered: address, reverse, and batch.

        References:
        http://www.mapquestapi.com/geocoding/
        http://www.mapquestapi.com/common/locations.html

        Params:
        {address}: an address (no place name support) *required
        {output}: the output type - 'json', 'xml', or 'csv'
        {return_coords_only}: return only (x, y) i.e. (LON, LAT) tuple - Boolean
        {mapquest_key}: a custom MapQuest Key; default is John's key - string

        Raw URL Example:
        http://www.mapquestapi.com/geocoding/v1/address?key=YOUR_KEY_HERE&locati
        on=1555%20Blake%20St%2C%20Denver%2C%20CO&outFormat=json&
        callback=renderGeocode

        Usage Limits:
        15,000 transactions per month

        Response:
        Returns multiple possible locations.
        """
        query = 'http://www.mapquestapi.com/geocoding/v1/address?key={mqkey}&'\
            'location={addr}&outFormat={out}&callback=renderGeocode'.format(
                mqkey=mapquest_key,
                addr=urllib.quote(address),
                out=output.lower())
        response = urllib.urlopen(query)
        data_string = ''
        for line in response:
            data_string += line
        data_string = data_string[14:-1]
        data_parsed = json.loads(data_string)
        if return_coords_only:
            if len(data_parsed['results'][0]['locations']) == 0:
                pprint("WARNING: Couldn't find the (x, y) coordinates.")
                return (0.0, 0.0)
            elif len(data_parsed['results'][0]['locations']) == 1:
                lat = data_parsed['results'][0]['locations'][0]['latLng']['lat']
                lon = data_parsed['results'][0]['locations'][0]['latLng']['lng']
                return (lon, lat)
            else:
                coords_list = []
                for resource in data_parsed['results'][0]['locations']:
                    lat = resource['latLng']['lat']
                    lon = resource['latLng']['lng']
                    coords_list.append((lon, lat))
                return coords_list
        else:
            return data_parsed

    def geocode_google(self, address, return_coords_only=False,
        google_key=_google_maps_browser_key):
        """Geocoding is the process of converting addresses, like '1600
        Amphitheatre Parkway, Mountain View, CA', into geographic coordinates,
        like {LAT=37.423021, LON=-122.083739}, which you can use to place
        markers or position the map.

        References:
        https://developers.google.com/maps/documentation/geocoding/intro

        Params:
        {address}: an address or place name, e.g. 'US Capitol' *required
        {return_coords_only}: return only (x, y) i.e. (LON, LAT) tuple - Boolean
        {google_key}: a custom Google Maps Key; default is John's key - string

        Raw URL Example:
        https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphithea
        tre+Parkway,+Mountain+View,+CA&key=YOUR_API_KEY

        Usage Limits:
        10 requests per second
        2,500 requests per day

        Response:
        Returns multiple possible locations.
        """
        gmaps = googlemaps.Client(google_key)
        json_data = gmaps.geocode(address)
        if len(json_data) == 0:
            pprint('WARNING: No location found')
            if return_coords_only:
                return (0.0, 0.0)
            else:
                return json_data
        if len(json_data) <= 1:
            if return_coords_only:
                lat = json_data['geometry']['location']['lat']
                lon = json_data['geometry']['location']['lng']
                return (lon, lat)
            else:
                return json_data[0]
        else:
            if return_coords_only:
                coords_list = []
                for response in json_data:
                    lat = response['geometry']['location']['lat']
                    lon = response['geometry']['location']['lng']
                    coords_list.append((lon, lat))
                return coords_list
            else:
                pprint('NOTE: Multiple matches found - *returned in a list*')
                return json_data

    def geocode_geocodio(self, address, return_coords_only=False,
        geocodio_key=_geocodio_app_key):
        """Geocoding (also known as forward geocoding) allows you to convert one
        or more addresses into geographic coordinates (i.e. latitude and
        longitude). Geocoding will also parse the address and append additional
        information (e.g. if you specify a zip code, Geocodio will return the
        city and state corresponding the zip code as well). Geocodio supports
        geocoding of addresses, cities and zip codes in various formats.

        References:
        https://geocod.io/docs/?python#introduction

        Params:
        {address}: an address (no place name support) *required
        {return_coords_only}: return only (x, y) i.e. (LON, LAT) tuple - Boolean
        {geocodio_key}: a custom Geocodio Key; default is John's key - string

        Raw URL Example:
        https://api.geocod.io/v1/geocode?q=10%20Beckett%20Street%2C%20Williamsto
        wn%2C%20VT%2005679&api_key=000ff728aa2fd8ae7737572b0afa5ef50d05dae

        Usage Limits:
        2,500 address lookups per day

        Response:
        Returns multiple *duplicate* instances of the same best-match location.
        """
        query = 'https://api.geocod.io/v1/geocode?q={addr}&api_key={geokey}'\
            .format(
                geokey=geocodio_key,
                addr=urllib.quote(address))
        response = urllib.urlopen(query)
        data_string = ''
        for line in response:
            data_string += line
        data_string = data_string
        data_parsed = json.loads(data_string)
        if return_coords_only:
            if len(data_parsed['results']) == 0:
                pprint('WARNING: No location found')
                return (0.0, 0.0)
            elif len(data_parsed['results']) == 1:
                lat = data_parsed['results'][0]['location']['lat']
                lon = data_parsed['results'][0]['location']['lng']
                return(lon, lat)
            else:
                coords_list = []
                for response in data_parsed['results']:
                    lat = response['location']['lat']
                    lon = response['location']['lng']
                    coords_list.append((lon, lat))
                return coords_list
        else:
            return data_parsed

    @classmethod
    def walk_tags(cls, response):
        """Flattens all keys in a parsed JSON object. Only keys with string,
        int, long, or float values are returned. Nested lists and tuples are
        walked into, but not returned. This is problematic for Bing coordinates,
        which are stored in a [Lat, Lon] list. Needs work for conflicting tags -
        current takes the last one (e.g. 'lat' and 'lon', which may come from
        the bounding box rather than the centroid.
        """
        def _walk(data):
            """Recursive inner function. Lots of type-checking that should
            ideally be duck-typed or use EAFP. This code could be beter.
            """
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, basestring) or \
                       isinstance(value, float) or \
                       isinstance(value, int) or \
                       isinstance(value, long):
                        flat_dict[key] = value
                    elif isinstance(value, list) or isinstance(value, tuple):
                        for item in value:
                            _walk(item)
                    elif isinstance(value, dict):
                        _walk(value)
            elif isinstance(data, list) or isinstance(data, tuple):
                for item in data:
                    _walk(item)
        flat_dict = {}
        _walk(response)
        return flat_dict

def main():
    """Test Functionality of script."""
    
    # Random Deloitte Offices as Tests
    orig = '1725 Duke Street, Alexandria, VA 22314-3456'
    wayp1 = 'US National Arboretum in Washington, DC'
    wayp2 = '2 15th Street NW, Washington, DC 20002'
    wayp3 = 'Monticello near Charlottesville, VA'
    dest = '7900 Tysons One Place, McLean, VA 22102-5971'

    origs = ['100 S. Charles Street, Baltimore, MD 21201-2713',
             '6810 Deerpath Road, Elkridge, MD 21075',
             '22454 Three Notch Road, Lexington Park, MD 20653']
    dests = ['1700 Market Street, Philadelphia, PA 19103-3984',
             '5 Walnut Grove Drive, Horsham, PA 19044',
             '1 Braxton Way, Glen Mills, PA 19342']

    geo = Geotool()

    # Google Maps Test
    response_google = geo.geocode_google(orig)

    # Bing Maps Test
    response_bing = geo.geocode_bing(wayp1)

    # Geocodio Test
    response_geocodio = geo.geocode_geocodio(wayp2)

    # MapQuest Test
    response_mapquest = geo.geocode_mapquest(dest)

    # ESRI Test
    response_esri = geo.geocode_esri(wayp3)

if __name__ == '__main__':
    ##main() # Don't consume my credits unless needed
    pass
