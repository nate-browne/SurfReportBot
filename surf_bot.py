#!/usr/local/bin/python2

import requests
import json
import time

class surf_bot:

    # spot ID's for Horseshoe beach La Jolla and 36th Street Newport Beach
    la_jolla = 4210
    newport = 4683

    """
    Constructor. Gets the api key and url for usage in other files
    """
    def __init__(self):

        # get the secret key
        with open(".secret", 'r') as inputfile:

            self.api_key = int(inputfile.read())

        # Set the url for getting the info
        self.apistr = "http://magicseaweed.com/api/%d/forecast/?spot_id=%d&units=uk"

    """
    Grabs the raw JSON data for parsing
    return: the JSON data parsed for la jolla and newport beach
    """
    def grab_data(self):

        lajolla_str = self.apistr % (self.api_key, surf_bot.la_jolla)
        newport_str = self.apistr % (self.api_key, surf_bot.newport)

        request1 = requests.get(lajolla_str)
        request2 = requests.get(newport_str)

        lajolla_data = request1.json()
        newport_data = request2.json()

        return lajolla_data[:1], newport_data[:1]

    """
    Extracts the rating information and prints it out to the screen
    params: data1 - JSON surf data to parse
    """
    def get_rating(self, data):

        solid_rating = data['solidRating']
        faded_rating = data['faded_rating']
        avg_rating = (solid_rating + faded_rating) / 2
        print "Solid rating: %d, faded rating: %d, average rating: %d" % (solid_rating, faded_rating, avg_rating)
        print

    """
    Extracts the swell information and prints it out to the screen
    params: data1 - JSON surf data to parse
    """
    def get_swell(self, data):

        min_height = data['swell']['minBreakingHeight']
        max_height = data['swell']['maxBreakingHeight']
        direction = data['swell']['components']['compassDirection']

        print "Swell height: %d (min), %d (max) in a %s direction" % (min_height, max_height, direction)
        print

    """
    Extracts the wind information and prints it out to the screen
    params: data1 - JSON surf data to parse
    """
    def get_wind(self, data):

        speed = data['wind']['speed']
        direction = data['wind']['direction']
        compass = data['wind']['compassDirection']

        print "Wind info: %d mph in a %d (%s) direction." % (speed, direction, compass)
        print

    """
    Calls helper functions to print the relevant data from the JSON.
    param: data1 - JSON object to parse
    param: data2 - JSON object to parse
    """
    def print_results(self, data1, data2):

        print "Local time: %s" % time.ctime(int(data1['localTimestamp']))

        print
        print "*" * 55
        print "Horseshoe Beach (Hospitals)"
        print "*" * 55
        print

        self.get_rating(data1)
        self.get_swell(data1)
        self.get_wind(data1)

        print
        print "*" * 55
        print "36th Street Newport Beach"
        print "*" * 55
        print

        self.get_rating(data2)
        self.get_swell(data2)
        self.get_wind(data2)
