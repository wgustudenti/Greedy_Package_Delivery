# Isaiah Bowers 001206471

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import copy
from datetime import timedelta

import PackageHash
from Distance import Distance
from Package import Package
from Truck import Truck


Truck.insertcorrectedaddress(9, "410 S State St", "Salt Lake City", "UT", "84111")

# Returns the package with the status given by the user
# Time = (O)n
# Space = (O)n
def lookuppackagebystatus(status):
    packagelist = []
    for bucket in Truck.packagehashtable.table:
        for item in bucket:
            if item[1].status == status:
                packagelist.append(item[1])
    return packagelist

# Returns the package with the weight given by the user
# Time = (O)n
# Space = (O)n
def lookuppackagebyweight(weight):
    packagelist = []
    for bucket in Truck.packagehashtable.table:
        for item in bucket:
            if item[1].weight == weight:
                packagelist.append(item[1])
    return packagelist

# Returns the package with the zipcode given by the user
# Time = (O)n
# # Space = (O)n
def lookuppackagebyzipcode(zipcode):
    packagelist = []
    for bucket in Truck.packagehashtable.table:
        for item in bucket:
            if item[1].zipcode == zipcode:
                packagelist.append(item[1])
    return packagelist

# Returns the package with the city given by the user
# Time = (O)n
# # Space = (O)n
def lookuppackagebycity(city):
    packagelist = []
    for bucket in Truck.packagehashtable.table:
        for item in bucket:
            if item[1].city == city:
                packagelist.append(item[1])
    return packagelist

# Returns the package with the deadline given by the user
# Time = (O)n
# # Space = (O)n
def lookuppackagebydeadline(deadline):
    packagelist = []
    for bucket in Truck.packagehashtable.table:
        for item in bucket:
            if item[1].deadlie == deadline:
                packagelist.append(item[1])
    return packagelist

# Returns the package with the address given by the user
# Time = (O)n
# # Space = (O)n
def lookuppackagebyaddress(address):
    packagelist = []
    for bucket in Truck.packagehashtable.table:
        for item in bucket:
            if item[1].address == address:
                packagelist.append(item[1])
    return packagelist

# Returns the package with the id given by the user
# Time = (O)n
# # Space = (O)n
def lookuppackagebyid(id):
    bucket = int(id) % 10
    for item in Truck.packagehashtable.table[bucket]:
        if item[1].id == id:
            itemlist = [item[1]]
            return itemlist

# Returns packages assocatiated with certain criteria.
# Time = (O)n
# Space = (O)n
def lookuppackages(typeofsearch, searchcriteria):
    if typeofsearch == "id":
            return lookuppackagebyid(searchcriteria)
    elif typeofsearch == "address":
            return lookuppackagebyaddress(searchcriteria)
    elif typeofsearch == "deadline":
            return lookuppackagebydeadline(searchcriteria)
    elif typeofsearch == "city":
            return lookuppackagebycity(searchcriteria)
    elif typeofsearch == "zipcode":
            return lookuppackagebyzipcode(searchcriteria)
    elif typeofsearch == "weight":
            return lookuppackagebyweight(searchcriteria)
    elif typeofsearch == "status":
            return lookuppackagebystatus(searchcriteria)


# Puts the trucks, packages, and drivers through the day's work, from start to finish.
# Time = (O)n3
# Space = (O)n
def completework():
    resettrucks()
    Truck.packagehashtable.populatenewpackagetable()
    truck1.loadtruck()
    truck2.loadtruck()
    while checkifworkatall():
        truck1.delivernextpackage()
        truck2.delivernextpackage()
    return Truck.packagehashtable.table

# Returns true if there is any work at all left to do during a specific day.
def checkifworkatall():
    if len(Truck.getremainingpackages()) != 0 or len(truck1.items) != 0 or len(truck2.items) != 0 \
            or len(truck3.items) != 0:
        return True
    else:
        return False

# Returns false if there's work to be done for a specific truck.
def checkifworkfortruck(truck):
    if len(Truck.getremainingpackages()) != 0 or len(truck.items) != 0:
        return True
    else:
        return False

#resets the trucks to how they were when the program started.
# Time = (O)n3
# Space = (O)n
def resettrucks():
    truck1.__init__(1)
    truck2.__init__(2)
    truck3.__init__(3)

def presentoneitem(package):
    presentation = [["Package ID", "Address", "City", "State", "Zipcode", "Deadline", "Weight", "Special Notes", "Status"]]
    presentation.append([package.id, package.address, package.city, package.state, package.zipcode, package.deadline,
                    package.weight, package.special, str(package.status) + " " + str(package.deliverytime)])
    return presentation

def presentallinfo(packagehashtable):
    presentation = [["Truck 1 Miles Travelled = " + str(truck1.distancetravelled)]]
    presentation.append(["Truck 2 Miles Travelled = " + str(truck2.distancetravelled)])
    presentation.append(["Truck 3 Miles Travelled = " + str(truck3.distancetravelled)])
    presentation.append([["Package ID", "Address", "City", "State", "Zipcode", "Deadline", "Weight", "Special Notes", "Status"]])
    for row in packagehashtable:
        for cell in row:
            onepackageinfo = []
            onepackageinfo.append(cell[1].id)
            onepackageinfo.append(cell[1].address)
            onepackageinfo.append(cell[1].city)
            onepackageinfo.append(cell[1].state)
            onepackageinfo.append(cell[1].zipcode)
            onepackageinfo.append(cell[1].deadline)
            onepackageinfo.append(cell[1].weight)
            onepackageinfo.append(cell[1].special)
            onepackageinfo.append(str(cell[1].status) + " " + str(cell[1].deliverytime))
            presentation.append(onepackageinfo)
    return presentation

# Presents address data for time snapshot
# This is not how incorrect addresses are updated for deliverypurposes.
def updateaddresstimesnapshot(time, hashtable):
    for bucket in hashtable:
        for cell in bucket:
            package = cell[1]
            if "Wrong address" in package.special:
                if package.timeavailable <= time:
                    for address in Truck.correctedaddresslist:
                        if int(address[0]) == int(package.id):
                            package.address = address[1]
                            package.city = address[2]
                            package.state = address[3]
                            package.zipcode = address[4]

# Returns a snapshot of the statuses of various elements for WGUPS at a certain time.
def timesnapshot(time):
    resettrucks()
    Truck.packagehashtable.populatenewpackagetable()
    truck1.loadtruck()
    truck2.loadtruck()
    timeforsnapshot = Package.gettimedelta(time)
    hashbackup = copy.deepcopy(Truck.packagehashtable)
    while truck1.currenttimeunknownaddress < timeforsnapshot and checkifworkfortruck(truck1):
        hashbackup = copy.deepcopy(Truck.packagehashtable)
        truck1.delivernextpackage()
    if checkifworkfortruck(truck1) or truck1.currenttimeunknownaddress > timeforsnapshot:
        Truck.packagehashtable = hashbackup
    while truck2.currenttimeunknownaddress < timeforsnapshot and checkifworkfortruck(truck2):
        hashbackup = copy.deepcopy(Truck.packagehashtable)
        truck2.delivernextpackage()
    if checkifworkfortruck(truck2) or truck2.currenttimeunknownaddress > timeforsnapshot:
        Truck.packagehashtable = hashbackup
    updateaddresstimesnapshot(timeforsnapshot, Truck.packagehashtable.table)
    return Truck.packagehashtable.table

def printpackagesontrucks():
    for item in truck1.items:
        print("Truck 1 item: " + str(item.id))
    for item in truck2.items:
        print("Truck 2 item: " + str(item.id))

truck1 = Truck(1)
truck2 = Truck(2)
truck3 = Truck(3)

donotexit = True

while(donotexit):
    try:
        print("1 = Look up one package or a group of packages at a specific time.")
        print("2 = Look up all packages and trucks at a specific time.")
        print("3 = Show all packages and trucks when everything is delivered.")
        print("4 = Close program.")
        choice = input("What would you like to do (1, 2, 3, or 4)? ")
        print("\n")
        if choice == "1":
            print("\n")
            print("Choices are: id, address, deadline, city, zipcode, weight, status")
            print("\n")
            type = input("What type of search would you like to run? ")
            print("\n")
            time = input("At what time would you like to lookup the package? Use form HH:MM.  Use 24 hr time. ")
            print("\n")
            criteria = input("Input what you would like to search (e.g. 5, if you are searching by id). ")
            a = lookuppackages(type, criteria)
            timesnapshot(time)
            for package in lookuppackages(type, criteria):
                for line in presentoneitem(package):
                    print(line)
        elif choice == "2":
            print("\n")
            time = input("Enter desired snapshot time in the form HH:MM.  Use 24 hr time. ")
            print(time)
            for line in presentallinfo(timesnapshot(time)):
                print(line)
            print("\n")
        elif choice == "3":
            print("\n")
            for line in presentallinfo(completework()):
                print(line)
            print("\n")
        elif choice == "4":
            print("\n")
            donotexit = False
            completework()
            print("Truck 1 total miles travelled = " + str(truck1.distancetravelled))
            print("Truck 2 total miles travelled = " + str(truck2.distancetravelled))
            print("Truck 3 total miles travelled = " + str(truck3.distancetravelled))
            print("Have a nice day!")
        else:
            print("That's not a choice!")
            print("\n")
    except(Exception):
        print("Something was entered incorrectly!  This program uses 24 hr time with precision to the minute.")
        print("\n")






