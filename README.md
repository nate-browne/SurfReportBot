# SurfReportBot

## Bringing the Surf Report to a Terminal Near You

![Ripping](https://bodyboard-holidays.com/wp-content/uploads/photo-gallery/imports//Indonesia%20Waves/scar_barrel.jpg)

### Intro
I love the beach. There's really nothing like the feeling of dropping in,
stalling a bit, getting tubed, then flying out of the barrel to the cheers of
your mates from the lineup.

Unfortunately, I can't always be out there to surf every great swell, but I
still like keeping up with swell patterns to be able to see what I'm missing and
to see if it'd be worth trying to get a session in later that day.

This project uses the MagicSeaweed API to get the current surf report and report
it to me to assist with those mind surf sessions that happen when I'm sitting at
my desk.

### Usage
To get started, just run this script from your .bashrc/.zshrc/whatever shell you
use. That's it. Really, that's it.

...sort of. You'll need to get your own API key from the dudes over at
[MagicSeaweed](https://magicseaweed.com/developer/terms-and-conditions), but
after you do that, go ahead and put it __*by itself*__ in a file called
`.secret`. Make sure that you have python 2 installed, along with the `requests`
module. If you don't have the latter, use the command `pip install requests` to
handle that. Lastly, make sure to change the first line of both scripts to be
`#!/usr/bin/env python` instead of the current `#!/usr/local/bin/python2`!
~~Make sure that that file is in the same directory as this script, as well as
in any directory that you'll call this script from (so if it's in your .rc files,
your `~` directory). The script will handle the rest :)~~

**UPDATE**: As of version 1.5, you only need a `.secret` in your home directory! Yay!
:)

### Credits
Cheers to MagicSeaweed for providing this sick API for using. You are the
best!

Want more information in the forecast? Feel free to submit an issue and I'll look
into adding it!

![Magic Seaweed Logo](https://im-1-uk.msw.ms/msw_powered_by.png)
