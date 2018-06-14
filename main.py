#!/usr/local/bin/python2

import surf_bot as sb

bot = sb.surf_bot()

def main():

    res = raw_input("Do you want the current surf data? (y)es or (n)o: ")

    if res.upper() == "Y" or res.upper() == "YES":

        json1, json2 = bot.grab_data()

        bot.print_results(json1, json2)

    else:

        print "Okay, maybe next time!"

if __name__ == '__main__':
    main()
