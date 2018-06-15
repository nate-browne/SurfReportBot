#!/usr/local/bin/python2
# Author: Nate Browne
# Version: 1.0
# Date: 15 Jun 2018
# File: main.py
# This is the main program driver for the surf bot. It uses the surf bot class
# to grab the data, then cleans it up before using the surf bot to output the
# relevant surf data

# Imports
import surf_bot as sb
import pprint
from datetime import datetime, timedelta
from time import ctime
from sys import argv, exit

def main():

    loc_str = 'localTimestamp'
    api_str = "http://magicseaweed.com/api/%s/forecast/?spot_id=%d&units=uk"

    # Set debug boolean
    debug = False

    # Enable debug mode
    if len(argv) > 1 and argv[1] == '-x':

        pp = pprint.PrettyPrinter(indent=1)
        debug = True

    # Create a surf bot object
    bot = sb.surf_bot(api_str, debug)

    print

    # Get the current day of the week
    curr_date = datetime.now()
    today = curr_date.strftime("%a")

    # Prompt you to see if you want the report. Helps so that you don't have to
    # see it if you don't want to
    res = raw_input("Do you want the current surf data? (y)es or (n)o: ")
    print

    if res.upper() == "Y" or res.upper() == "YES":

        # Make API call to grab JSON surf data
        json1, json2 = bot.grab_data()

        # Verify that we got something back
        if json1 == None or json2 == None:

            print "Exiting..."
            exit(1)

        # Get the reports for today
        loc1 = [obj for obj in json1 if today in ctime(obj[loc_str])]
        loc2 = [obj for obj in json2 if today in ctime(obj[loc_str])]

        # Grab first chart in json object as a preliminary step
        r1 = loc1[0]

        # Get the most recent chart (to the current time)
        for chrt in loc1:

            # Create timedelta objects by subtracting timestamps
            res = abs(curr_date - datetime.fromtimestamp(chrt[loc_str]))
            prev = abs(curr_date - datetime.fromtimestamp(r1[loc_str]))

            # Smaller # of seconds == closer to current time
            if res.total_seconds() < prev.total_seconds():

                r1 = chrt

        # Grab first chart in json object as a preliminary step
        r2 = loc2[0]

        # Get the most recent chart (to the current time)
        for chrt in loc2:

            # Create timedelta objects by subtracting timestamps
            res = abs(curr_date - datetime.fromtimestamp(chrt[loc_str]))
            prev = abs(curr_date - datetime.fromtimestamp(r2[loc_str]))

            # Smaller # of seconds == closer to current time
            if res.total_seconds() < prev.total_seconds():

                r2 = chrt

        # All good, let's get the surf report!
        bot.print_results(r1, r2)

    else:

        print "Okay, maybe next time!"
        print

# Standard Boilerplate Code to run main()
if __name__ == '__main__':
    main()
