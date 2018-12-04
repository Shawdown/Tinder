from tinder_api_sms import *

while(1):
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
