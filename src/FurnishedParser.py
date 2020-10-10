import urllib.request
import random
import time
import re

from datetime import date

FURNISHED_URL = "https://www.furnished.lu/index.php?route=product/product&product_id=%d"
MAX_RESIDENCE_NUMBER = 10000
MAX_FAIL_READ = 100
MARKER_SHIFT = 0.00002
MARKER_SPREAD = 5
SLEEP_TIME = 0.001

marketPositions = {123, 124}


def parsePage(document, residenceId):
    #print(document)
    residenceId = "Id : " + residenceId.__str__()
    locationInitialization = re.search("new google.maps.LatLng(.*)", document).group()
    location = re.search("'[0-9]+.[0-9]*', '[0-9]+.[0-9]*'", locationInitialization).group()
    location = re.sub("'", '', location)
    locationX = float(re.search("[0-9]+.[0-9]*", location).group())
    locationY = re.search(", [0-9]+.[0-9]*", location).group()
    locationY = float(re.sub(", ", "", locationY))
    residenceName = re.sub(' +', ' ', re.search("<h1>Residence : .*</h1>", document).group())
    residenceName = nomalize(residenceName)
    residencePice = re.search("<h2 class=\"wk-search-title\">(\r\n|\r|\n)*.*</h2>", document).group()
    residencePice = nomalize(residencePice)
    residencePice = "Price : " + re.sub('<h2 class="wk-search-title"> ', '', residencePice)
    checkIn = re.search("<option data-checkout=checkin-0.*value=\".*\">", document).group()
    checkIn = nomalize(checkIn)
    checkIn = "CheckIn : " + re.sub('<option data-checkout=checkin-0 value="|">', '', checkIn)
    residenceSize = re.search("[0-9]+(,|[0-9])*m<sup>2</sup>", document).group()
    residenceSize = "Size : " + re.sub('<sup>2</sup>', '', residenceSize) + "^2"

    #print(location)
    #print(residenceName)
    #print(residencePice)
    #print(checkIn)
    #print(residenceSize)
    locationX = spreadPosition(locationX)
    locationY = spreadPosition(locationY)
    return [residenceId + "\n" + residenceName + "\n" + residencePice + "\n" + residenceSize + "\n" + checkIn, locationX, locationY, 1]


def spreadPosition(position):
    newPosition = position
    while marketPositions.__contains__(newPosition):
        newPosition = position + MARKER_SHIFT * random.random()
    marketPositions.add(newPosition)
    return newPosition


def nomalize(str):
    str = re.sub(' +', ' ', str)
    return re.sub('<h1>|<h2>|</h1>|</h2>|(\r\n|\r|\n|\t)', '', str)


def writeToFile(str):
    text_file = open(date.today().__str__(), "w")
    n = text_file.write(str)
    text_file.close()

def main():
    random.seed(MARKER_SPREAD)
    failAttemps = 0
    residences = []
    for id in range(659, MAX_RESIDENCE_NUMBER):
        time.sleep(SLEEP_TIME)
        print(id)
        if failAttemps > 40:
            break
        pageUrl = FURNISHED_URL % id
        try:
            page = urllib.request.urlopen(pageUrl)
            if (page.getcode() == 200):
                failAttemps = 0
                residence = parsePage(page.read().decode("utf-8"), pageUrl)
                residences.append(residence)
            else:
                failAttemps += 1
        except Exception as e:
            print(e)
            failAttemps += 1

    residences = residences.__str__() + ";"
    writeToFile(residences)
    print(residences)


if __name__ == "__main__":
    main()
