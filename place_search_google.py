import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import json
from time import sleep
pd.set_option('max_colwidth', 100)

def extract_address(keyword, API_KEY, coordinates=None, radius = '8047'):
    
    """
    Returns a dataframe containing information about a set of places based on the keyword

    Parameters
    ----------
    keyword : str (required)
        parameter for the search. Replace all spaces with +.
        example include "grocery+stores", "restaurants", "italian+food" etc.
        
    API_KEY: str (required)
        your google maps api_key 
    
    coordinates: str (optional)
        latitude and longitude seperated by a comma, e.g, '39.8000659,-86.302886'
        results based on your location when coordinates not specified
    
    radius: str (optional)
        search restricted to 5 miles/8000 meters.
        Maximum allowed radius is 50,000 meters by googleapi.
        
    Returns
    -------
    DataFrame
        A dataframe containing two columns - name and address.

    """
    if coordinates is not None:
        base_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'+'query='+keyword+'&location='+coordinates+'&radius='+radius+'&key='+API_KEY
    else:
        base_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'+'query='+keyword+'&radius='+radius+'&key='+API_KEY
    #print(base_url)
    
    data_list = []
    url = base_url
    print('Requesting access')
    while True:
        response = requests.get(url)
        #a request will have a status code of 200 if valid and 404 if invalid
        if response.status_code == 404:
            print('url is not valid. Please check the address')
            return
        data_dump = json.loads(response.text)
        results = data_dump['results']
        if len(results) == 0:
            print('No results found for the query. Are you sure the keyword is correct?')
        for result in results:
            data_list.append([result['name'],result['formatted_address']])
        #check to see if the results are more than one page long using next_page_token key from the json
        if 'next_page_token' not in data_dump.keys():
            break
        url = base_url +'&pagetoken='+data_dump['next_page_token']
        #print(url)
        print('Requesting access - next page')
        sleep(10) #to avoid bombarding the server with back to back requests
        
    data_df = pd.DataFrame(data_list, columns=['name', 'address'])
    return data_df
        