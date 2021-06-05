from datetime import datetime

DATE_FORMAT = "%Y-%m-%d"

def convertToMap(strMap):
    #Do not save data as you did before, I need to make additional converter now (
    map = strMap[2:-3]
    list = map.split("], [")
    map = []
    for strRecord in list:
        strRecord = strRecord.split(", ")
        record = {}
        info = strRecord[0].split("\\n")
        record["locationX"] = float(strRecord[1])
        record["locationY"] = float(strRecord[2])
        record["residenceId"] = info[0].split(" : ")[1]
        record["residenceName"] = info[1].split(" : ")[1]
        record["residencePrice"] = info[2].split(" : ")[1].split("&")[0].replace(",", "")
        record["residenceSize"] = info[3].split(" : ")[1].split("m")[0].replace(",", ".")
        record["checkIn"] = info[4].split(" : ")[1].replace("'", "")
        map.append(record)
    return map


def readFromFile(filePath):
    text_file = open(filePath, "r")
    map = text_file.read()
    text_file.close()
    return convertToMap(map)


def convertToMapMark(record):
    return [record["residenceId"] + "\n" + record["residenceName"] + "\n" + record["residencePrice"] + "\n"
                  + record["residenceSize"] + "\n" + record["checkIn"], record["locationX"], record["locationY"], 1]


def createMapMarks(residences):
    result = []
    for record in residences:
        result.append(convertToMapMark(record))
    return result.__str__() + ";"


def priceSort(e):
    return float(e["residencePrice"])


def priceMeterSort(e):
    return float(e["residencePrice"]) / float(e["residenceSize"])


def main():
    map = readFromFile("./2021-06-04")
    residencesCheapest = map.copy()
    residencesCheapest.sort(reverse=False, key=priceSort)
    residencesExpensive = map.copy()
    residencesExpensive.sort(reverse=True, key=priceSort)
    myCheckIn = datetime.strptime("2021-09-01", DATE_FORMAT)
    residencesPricePerMeter = map.copy()
    residencesPricePerMeter.sort(reverse=False, key=priceMeterSort)
    residences = []
    for record in map:
        residencePrice = float(record["residencePrice"])
        residenceSize = float(record["residenceSize"])
        residenceCheckIn = datetime.strptime(record["checkIn"], DATE_FORMAT)
        if residencePrice <= 700 and residenceSize > 12 and residenceCheckIn < myCheckIn:
            residences.append(record)
    print("-------------Residences Preference----------------")
    print(createMapMarks(residences))
    print()
    print("-------------Top 10 most expensive Residences----------------")
    print(createMapMarks(residencesExpensive[:10]))
    print()
    print("-------------Top 10 most cheapest Residences----------------")
    print(createMapMarks(residencesCheapest[:10]))
    print()
    print("-------------Top 10 price/meters Residences----------------")
    print(createMapMarks(residencesPricePerMeter[:10]))
    print()


if __name__ == "__main__":
    main()