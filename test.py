from tinder_api_sms import *

# Functions

def saveJsonFormated(file, data):
    # now write output to a file
    fd = open(file, "w")
    # magic happens here to make it pretty-printed
    #json.dump(data, fd)
    fd.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
    fd.close()

# Main code

#
# Saving all matches to a file
#
print("matches count: " + str(len(all_matches(100)["data"]["matches"])))

saveJsonFormated("tinder-data/matches.json", all_matches(100)["data"]["matches"])

while 1:
    rec = get_recommendations()

    likedTotal = 0

    try:
        print("Found " + str(len(rec["results"])) + " girls.")

        for girl in rec["results"]:
            like(girl["_id"])
            print("Liked.")
            print("id=" + girl["_id"])
            print("name=" + girl["name"])
            likedTotal += 1

    except Exception as e:
        print("Found no girls")
        break

    print("Liked " + str(likedTotal) + " girls")
