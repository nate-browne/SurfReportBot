#!/usr/local/bin/python2

import surf_bot as sb
import pprint
from datetime import datetime
from time import ctime, time
from sys import argv


def main():

    # Set debug boolean
    debug = False

    # Create a surf bot object
    bot = sb.surf_bot()

    # Enable debug mode
    if len(argv) > 1 and argv[1] == '-x':

        pp = pprint.PrettyPrinter(indent=1)
        debug = True

    print

    # Get the current day of the week
    curr_date = datetime.now()
    today = curr_date.strftime("%a")

    # Get the current UNIX time
    curr_time = int(time())

    # Print the current UNIX time if in debug mode
    if debug == True:
        print curr_time

    # Prompt you to see if you want the report. Helps so that you don't have to
    # see it if you don't want to
    res = raw_input("Do you want the current surf data? (y)es or (n)o: ")

    if res.upper() == "Y" or res.upper() == "YES":

        json1, json2 = bot.grab_data()

        # Get a list of today's surf charts for both locations
        d1 = [obj for obj in json1 if today in ctime(int(obj['localTimestamp']))]
        d2 = [obj for obj in json2 if today in ctime(int(obj['localTimestamp']))]

        # Parse the most recently published chart
        r1 = d1[0]
        for chrt in d1:

            diff = abs(curr_time - int(chrt['timestamp']))
            curr_diff = abs(curr_time - int(r1['timestamp']))

            if debug == True:
                print diff, curr_diff

            if diff < curr_diff:
                r1 = chrt

        # Parse the most recently published chart
        r2 = d2[0]
        for chrt in d2:

            diff = abs(curr_time - int(chrt['timestamp']))
            curr_diff = abs(curr_time - int(r2['timestamp']))

            if debug == True:
                print diff, curr_diff

            if diff < curr_diff:
                r2 = chrt

        # Print the times and the most recent chart JSON if debug is on
        if debug == True:
            print curr_time, r1['timestamp'], r2['timestamp']

        # All good, let's get the surf report!
        bot.print_results(r1, r2)

    else:

        print "Okay, maybe next time!"
        print

if __name__ == '__main__':
    main()
