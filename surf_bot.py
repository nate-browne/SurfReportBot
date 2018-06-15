#!/usr/local/bin/python2

import requests
import json
from time import localtime, strftime

class surf_bot:

    # spot ID's for Horseshoe beach La Jolla and 36th Street Newport Beach
    la_jolla = 4210
    newport = 4683

    """
    Constructor. Gets the api key and sets the url for usage
    """
    def __init__(self):

        # get the secret key
        with open(".secret", 'r') as inputfile:

            temp = inputfile.readline()

            # replace the newline char
            self.api_key = temp[:-1]

        # Set the url for getting the info
        self.apistr = "http://magicseaweed.com/api/%s/forecast/?spot_id=%d&units=uk"

    """
    Grabs the raw JSON data for parsing
    return: the JSON data parsed for la jolla and newport beach as two lists
    """
    def grab_data(self):

        # Fill in corresponding api call strings
        lajolla_str = self.apistr % (self.api_key, surf_bot.la_jolla)
        newport_str = self.apistr % (self.api_key, surf_bot.newport)

        # Get the corresponding webpages
        request1 = requests.get(lajolla_str)
        request2 = requests.get(newport_str)

        # Parse webpages as JSON
        lajolla_data = request1.json()
        newport_data = request2.json()

        # Filter so the return is only the first item in the list
        return lajolla_data, newport_data

    """
    Extracts the rating information and prints it out to the screen
    params: data - JSON surf data to parse
    """
    def get_rating(self, data):

        # Get the three valid kinds of ratings
        solid_rating = data['solidRating']
        faded_rating = data['fadedRating']
        avg_rating = (solid_rating + faded_rating) / 2

        # Print the results
        print "Solid rating: %d, faded rating: %d, average rating: %d." % (solid_rating, faded_rating, avg_rating)
        print

    """
    Extracts the swell information and prints it out to the screen
    params: data - JSON surf data to parse
    """
    def get_swell(self, data):

        # Grab the wave heights and direction of main swell component
        min_height = data['swell']['minBreakingHeight']
        max_height = data['swell']['maxBreakingHeight']
        direction = data['swell']['components']['combined']['compassDirection']

        # Grab direction and period of the primary swell component
        prim_dir = data['swell']['components']['primary']['compassDirection']
        prim_per = data['swell']['components']['primary']['period']

        # Grab direction and period of the secondary swell component
        sec_dir = data['swell']['components']['secondary']['compassDirection']
        sec_per = data['swell']['components']['secondary']['period']

        # print results
        print "Swell height: %d ft (min), %d ft (max) in a %s direction." % (min_height, max_height, direction)
        print "Primary component: %s direction with a swell period of %d." % (prim_dir, prim_per)
        print "Secondary component: %s direction with a swell period of %d." % (sec_dir, sec_per)

    """
    Extracts the wind information and prints it out to the screen
    params: data - JSON surf data to parse
    """
    def get_wind(self, data):

        # Grab wind speed and direction (both compass and degrees)
        spd = data['wind']['speed']
        drc = data['wind']['direction']
        comp = data['wind']['compassDirection']

        # print results
        print "Wind info: %d mph in a %d (%s) direction." % (spd, drc, comp)
        print

    """
    Calls helper functions to print the relevant data from the JSON.
    param: data1 - JSON object to parse
    param: data2 - JSON object to parse
    """
    def print_results(self, data1, data2):

        print
        print "*" * 55
        print "Horseshoe Beach (Hospitals)"
        print "*" * 55
        print

        # Print the time of the chart
        timestr = localtime(int(data1['issueTimestamp']))
        print "Time of chart: %s" % strftime("%a %d %b %Y at %H:%M:%S", timestr)
        print

        # Get information for La Jolla
        self.get_rating(data1)
        self.get_swell(data1)
        self.get_wind(data1)

        print "*" * 55
        print "36th Street Newport Beach"
        print "*" * 55
        print

        # Print the time of the chart
        timestr = localtime(int(data2['issueTimestamp']))
        print "Time of chart: %s" % strftime("%a %d %b %Y at %H:%M:%S", timestr)
        print

        # Get information for Newport Beach
        self.get_rating(data2)
        self.get_swell(data2)
        self.get_wind(data2)
