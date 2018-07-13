#!/usr/local/bin/python2
# Author: Nate Browne
# Version: 1.5
# Date: 15 Jun 2018
# Last Edited: 17 Jun 2018
# File: surf_bot.py
# This file contains the surf bot class which has the capability to make API
# calls, read in the API key, and parse the relevant data from the extracted
# JSON before outputting the results.

# Imports
import requests
import json
from time import localtime, strftime
from os.path import expanduser

class surf_bot(object):
    '''This class sets up the surf bot object.
    A surf_bot is comprised of spot IDs, an api key,
    and various functions used to grab the JSON, parse the JSON,
    and print out results to the user
    '''

    # Class variables

    # Spot IDs
    la_jolla = 4210
    newport = 4683

    # Printed strings
    swell_str = "Swell height: %d ft (min), %d ft (max) in a %s direction."
    comp1 = "Primary component: %s direction with a swell period of %d."
    comp2 = "Secondary component: %s direction with a swell period of %d."
    rating = "Solid rating: %d, faded rating: %d, average rating: %d."
    wind = "Wind info: %d mph in a %d (%s) direction."
    chrt_time = "Time of chart: %s"
    time_str = "%a %d %b %Y at %H:%M:%S"

    def __init__(self, apistr, debug):
        """Constructor. Gets the api key and sets the url for usage"""

        # get the secret key
        with open(expanduser("~/.secret"), 'r') as inputfile:

            # Read in the API key
            self.api_key = inputfile.readline().strip()

        # Set the url for getting the info
        self.apistr = apistr
        self.debug = debug

    def grab_data(self):
        """Grabs the raw JSON data for parsing"""

        # Fill in corresponding api call strings
        lajolla_str = self.apistr % (self.api_key, surf_bot.la_jolla)
        newport_str = self.apistr % (self.api_key, surf_bot.newport)

        # Get the corresponding webpages
        rq1 = requests.get(lajolla_str)
        rq2 = requests.get(newport_str)

        # Print status codes
        if self.debug:

            print "error codes: %d, %d" % (rq1.status_code, rq2.status_code)

        # Save good response code, for readability
        good = requests.codes['ok']

        # Handle error codes
        if rq1.status_code != good or rq2.status_code != good:

            print "Uh oh, something went wrong. Use debug mode for more info."
            return None, None

        # Parse webpages as JSON
        lajolla_data = rq1.json()
        newport_data = rq2.json()

        # Return the lists of JSON data for parsing
        return lajolla_data, newport_data

    def get_rating(self, data):
        """Extracts the rating information and prints it out to the screen
        param: data - JSON surf data to parse
        """

        # Get the three valid kinds of ratings
        solid_rating = data['solidRating']
        faded_rating = data['fadedRating']
        avg_rating = (solid_rating + faded_rating) / 2

        # Print the results
        print surf_bot.rating % (solid_rating, faded_rating, avg_rating)
        print

    def get_swell(self, data):
        """Extracts the swell information and prints it out to the screen"""

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
        print surf_bot.swell_str % (min_height, max_height, direction)
        print surf_bot.comp1 % (prim_dir, prim_per)
        print surf_bot.comp2 % (sec_dir, sec_per)

    def get_wind(self, data):
        """Extracts the wind information and prints it out to the screen"""

        # Grab wind speed and direction (both compass and degrees)
        spd = data['wind']['speed']
        drc = data['wind']['direction']
        comp = data['wind']['compassDirection']

        # print results
        print surf_bot.wind % (spd, drc, comp)
        print

    def print_results(self, data1, data2):
        """Calls helper functions to print the relevant data from the JSON."""

        print
        print "*" * 55
        print "Horseshoe Beach (Hospitals)"
        print "*" * 55
        print

        # Print the time of the chart
        chrt_time = localtime(data1['localTimestamp'])
        print surf_bot.chrt_time % strftime(surf_bot.time_str, chrt_time)
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
        chrt_time = localtime(data2['localTimestamp'])
        print surf_bot.chrt_time % strftime(surf_bot.time_str, chrt_time)
        print

        # Get information for Newport Beach
        self.get_rating(data2)
        self.get_swell(data2)
        self.get_wind(data2)
