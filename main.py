#!/usr/local/bin/python2

import surf_bot as sb

bot = sb.surf_bot()

def main():

    print

    # Prompt you to see if you want the report. Helps so that you don't have to
    # see it if you don't want to
    res = raw_input("Do you want the current surf data? (y)es or (n)o: ")

    if res.upper() == "Y" or res.upper() == "YES":

        json1, json2 = bot.grab_data()

        bot.print_results(json1[0], json2[0])

    else:

        print "Okay, maybe next time!"
        print

if __name__ == '__main__':
    main()
