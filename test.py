import time

from tinder_api_sms import *
#from tinder_api import *
from features import *

# Functions

def saveJsonFormated(file, data):
    # now write output to a file
    fd = open(file, "w")
    # magic happens here to make it pretty-printed
    #json.dump(data, fd)

    fd.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
    fd.close()

# Main code

sl = open("tinder-data/swipe-log.txt", "a+")

#
# Saving all matches to a file
#

matches = all_matches(100, True)["data"]["matches"]

print("matches count: " + str(len(matches)))

saveJsonFormated("tinder-data/matches.json", matches)
saveJsonFormated("tinder-data/1.json", get_person("shawdown"))

while 1:
    rec = get_recommendations()

    likedTotal = 0

    try:
        print("Found " + str(len(rec["results"])) + " girls.")

        for girl in rec["results"]:
            like(girl["_id"])
            likedTotal += 1

            logString = time.strftime("%x %X") + " | LIKE | [id=" + girl["_id"] + ", name=" + girl["name"] + "]\n"

            print(logString)

            sl.write(logString)
            pause()

    except Exception as e:
        print("Found no girls")
        break

    print("Liked " + str(likedTotal) + " girls")

sl.close()