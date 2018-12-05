import time
import os
import re

from tinder_api_sms import *
#from tinder_api import *
from features import *

# Functions

def getJsonFormatted(data):
    return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))


def saveJsonFormated(file, data):
    # now write output to a file
    fd = open(file, "w")
    # magic happens here to make it pretty-printed
    #json.dump(data, fd)

    fd.write(getJsonFormatted(data))
    fd.close()

# Main code

#
# Saving our profile info for the current session, if something in it has changed
#

# Finding the last file
lastSessionTime = ""
lastSessionFilename = ""

for filename in os.listdir('tinder-data/sessions-data'):
    rgx = re.compile("(\d+-\d+-\d+_\d+-\d+-\d+)\.json")
    matches = rgx.match(filename)

    if(matches == None):
        print("Filename [" + filename + "] is not a session data file. Skipping...")
        continue

    filetime = datetime.strptime(matches.group(1), '%Y-%m-%d_%H-%M-%S')

    if (lastSessionTime == "" or lastSessionTime < filetime):
        lastSessionTime = filetime
        lastSessionFilename = filename


self = get_self()

saveSession = True

if(lastSessionTime != ""):
    selfFormatted = getJsonFormatted(self)
    if selfFormatted == open("tinder-data/sessions-data/" + lastSessionFilename).read():
        print('No profile changes found. Skipping session data save...')
        saveSession = False

if(saveSession):
    saveJsonFormated("tinder-data/sessions-data/" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".json", self)

my_id = self["_id"]
my_name = self["name"]

#
# Saving all matches to a file
#
matches = get_updates()["matches"]
print("matches count: " + str(len(matches)))
saveJsonFormated("tinder-data/matches.json", matches)


#
# Saving messages for every match to it's own file
#
for match in matches:
    try:
        p = match["person"]
        mm = match["messages"]

        with open("tinder-data/matches-messages/" + match["person"]["name"] + "-" + match["person"]["_id"] + ".txt", "w", encoding='utf-8') as mf:
            for m in mm:
                mFrom = m["from"]
                mFromName = my_name if mFrom == my_id else p["name"]
                mTo = m["to"]
                mToName = my_name if mTo == my_id else p["name"]
                mText = m["message"]

                mf.write("From: " + mFromName + " [id=" + mFrom + "]\n")
                mf.write("To: " + mToName + " [id=" + mTo + "]\n")
                mf.write("Time: " + m["sent_date"] + "\n")
                mf.write("Text: [" + mText + "]\n\n")

    except Exception as e:
        print("Got an exception while saving match messages: " + str(e))
exit(2)
#
# We're starting to like people (LOL) and log it
#
sl = open("tinder-data/swipe-log.txt", "a+")

while 1:
    rec = get_recommendations()

    likedTotal = 0

    try:
        print("Found " + str(len(rec["results"])) + " people to like.")

        for girl in rec["results"]:
            #like(girl["_id"])
            likedTotal += 1

            logString = time.strftime("%x %X") + " | LIKE | [id=" + girl["_id"] + ", name=" + girl["name"] + "]\n"

            print(logString)

            sl.write(logString)
            pause()

    except Exception as e:
        print("Found no girls")
        break

    print("Liked " + str(likedTotal) + " people.")

sl.close()
