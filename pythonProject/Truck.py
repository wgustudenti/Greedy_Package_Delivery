from datetime import timedelta
from decimal import Decimal

import PackageHash
from Distance import Distance
from Package import Package


# Contains things having to do with the trucks
class Truck:
    packagehashtable = PackageHash.ChainingHashTable()
    packagehashtable.populatenewpackagetable()

    correctedaddresslist = []


    # Time = (O)1
    # Space = (O)1
    @staticmethod
    def insertcorrectedaddress(id, address, city, state, zipcode):
        correctedaddress = []
        correctedaddress.append(id)
        correctedaddress.append(address)
        correctedaddress.append(city)
        correctedaddress.append(state)
        correctedaddress.append(zipcode)
        Truck.correctedaddresslist.append(correctedaddress)

    # Represents the time the delayed packages become available.
    # Time = (O)n2
    # Space = (O)n
    delayedpackageavailablelist = []
    for row in packagehashtable.table:
        for column in row:
            if "Delayed" in column[1].special:
                if column[1].timeavailable != timedelta(hours=8):
                    if column[1].timeavailable not in delayedpackageavailablelist:
                        delayedpackageavailablelist.append(column[1].timeavailable)

    # Sets up a table of times packages are available
    # Time = (O)n
    # Space = (O)n
    timeavailabletable = []
    for row in packagehashtable.table:
        for column in row:
            onepackageaddresscombo = []
            onepackageaddresscombo.append(column[1].id)
            onepackageaddresscombo.append(column[1].timeavailable)
            timeavailabletable.append(onepackageaddresscombo)

    # Time: (O)1
    # Space: (O)1
    def __init__(self, idnumber):
        self.idnumber = idnumber
        self.items = []
        self.distancetravelled = 0
        self.currentlocation = "Western Governors University"
        self.mustdelivertogetherlist = []
        self.currenttimeunknownaddress = timedelta(hours=8)

    # Searches the hash table for packages still at the hub and returns a list of those packages.
    # Time = (O)n2
    # Space = (O)n
    @staticmethod
    def getremainingpackages():
        remainingpackages = []
        for listintable in Truck.packagehashtable.table:
            for keyvaluepair in listintable:
                if keyvaluepair[1].status == "at the hub":
                    remainingpackages.append(keyvaluepair[1])
        return remainingpackages

    # Returns true if before 9:05 (calculated from distancetraveled)
    # Else false
    # Time = (O)1
    # # Space = (O)1
    def checkdelays(self):
        if self.distancetravelled < 19.5:
            return True
        else:
            return False

    # Returns the current time according to the amount of miles travelled.
    # Time = (O)1
    # # Space = (O)1
    def getcurrenttimebymileage(self):
        timepassedinhours = (self.distancetravelled / 18)
        currenttime = timedelta(hours=float(8+timepassedinhours))
        return currenttime

    # Loads package with deadlines other than EOD onto the truck.
    # Time = (O)n2
    # # Space = (O)n
    def loaddeadline(self):
        while len(self.items) < 16:
            internallist = []
            for package in self.items:
                if package.deadline != "EOD":
                    internallist.append(package)
            if len(internallist) > 7:
                break
            if len(self.items) == 0:
                pseudocurrentlocation = "Western Governors University"
            else:
                pseudocurrentlocation = self.items[len(self.items)-1].address
            deadlinelist = []
            if len(self.items) < 16:
                for package in self.removedelays(Truck.getremainingpackages()):
                    if package.deadline != "EOD":
                        deadlinelist.append(package)
            if len(deadlinelist) != 0:
                nextpackage = Distance.getclosestpackagebyaddress(pseudocurrentlocation, deadlinelist)
                self.loadonepackage(nextpackage)
            else:
                break

    # Loads package with constraints concerning which truck they can be loaded onto.
    # Time = (O)n2
    # # Space = (O)n
    def loadtruckconstraints(self):
        if len(self.items) < 16:
            if self.idnumber == 2 and len(self.items) < 16:
                for package in self.removedelays(Truck.getremainingpackages()):
                    if "Can only be on truck 2" in package.special:
                        self.loadonepackage(package)

    # Loads package with constraints concerning other packages they must be delivered with.
    # Time = (O)n
    # # Space = (O)n
    def loaddeliveryconstraints(self):
        i = 0
        if len(self.items) < 16:
            for package in Truck.getremainingpackages():
                if "Must be delivered with" in package.special:
                    i = i + 1
        if len(self.items) < 16 and (16-len(self.items)) >= (16 - i):
            for package in Truck.getremainingpackages():
                if package.id == "13" or package.id == "14" or package.id == "15" or package.id == "16"\
                    or package.id == "19" or package.id == "20":
                    self.mustdelivertogetherlist.append(package)
                    self.loadonepackage(package)


    # Loads one package onto truck.  Updates status and hashtable.
    # Time = (O)n
    # # Space = (O)1
    def loadonepackage(self, package):
        package.status = "en route"
        self.items.append(package)
        Truck.packagehashtable.insert(package)

    # Loads any package using a greedy algorithm where the shortest delivery distance from last loaded package
    # is considered the best option.
    # Time = (O)n2
    # Space = (O)n
    def loadany(self):
        while len(self.items) < 16 and len(Truck.getremainingpackages()) != 0:
            if len(self.items) != 0:
                pseudolocation = self.items[len(self.items)-1].address
            else:
                pseudolocation = "Western Governors University"
            nextpackage = Distance.getclosestpackagebyaddress(pseudolocation, self.removedelays(Truck.getremainingpackages()))
            self.loadonepackage(nextpackage)

    # Takes a package list parameter and returns that list without packages that have unknown addresses
    # Time = (O)n3
    # Space = (O)n
    def removeunknownaddress(self, remainingpackages):
        listtoreturn = []
        for package in remainingpackages:
            listtoreturn.append(package)
        for time in Truck.timeavailabletable:
            if self.currenttimeunknownaddress < time[1]:
                for package in remainingpackages:
                    if "Wrong address" in package.special and self.currenttimeunknownaddress < package.timeavailable:
                        for otherpackage in listtoreturn:
                            if package.id == otherpackage.id:
                                listtoreturn.remove(otherpackage)
        for package in listtoreturn:
            if "Wrong address" in package.special:
                for address in Truck.correctedaddresslist:
                    if int(address[0]) == int(package.id):
                        package.address = address[1]
                        package.city = address[2]
                        package.state = address[3]
                        package.zipcode = address[4]
        return listtoreturn

    # Takes a list of packages and removes the packages that were delayed until
    # such time as they are available.
    # Time = (O)n
    # Space = (O)n
    def removedelays(self, remainingpackages):
        listtoreturn = []
        for package in remainingpackages:
            listtoreturn.append(package)
        for time in Truck.delayedpackageavailablelist:
            if self.currenttimeunknownaddress < time:
                for package in remainingpackages:
                    if "Delayed" in package.special and self.currenttimeunknownaddress < package.timeavailable:
                        listtoreturn.remove(package)
        return listtoreturn

    # Master load function that calls all other load functions.
    # Time = (O)n2
    # Space = (O)n
    def loadtruck(self):
        self.loaddeliveryconstraints()
        self.loaddeadline()
        self.loadtruckconstraints()
        self.loadany()

    # Delivers one package, updates status, delivery time, distance traveled, and hashtable.
    # Time = (O)n
    # Space = (O)n
    def deliveronepackage(self, package):
        distance = Distance.getdistancebetweenbyaddress(self.currentlocation, package.address)
        package.status = "delivered"
        self.distancetravelled = self.distancetravelled + Decimal(distance)
        self.currenttimeunknownaddress = self.currenttimeunknownaddress + timedelta(hours=float(Decimal(distance)/18))
        package.deliverytime = self.currenttimeunknownaddress
        Truck.packagehashtable.insert(package)
        self.currentlocation = package.address
        self.items.remove(package)

    # Returns true if there is a package with a deadline other than EOD loaded on the truck, else false.
    # Time = (O)n
    # Space = (O)n
    def checkifdeadlines(self):
        for package in self.items:
            if package.deadline != "EOD":
                return True
        return False

    # Returns true if any delayed packages have not yet been loaded onto a truck.
    # Else false.
    # Time = (O)n
    # Space = (O)n
    @staticmethod
    def checkifdelaysremain():
        for package in Truck.getremainingpackages():
            if "Delayed" in package.special:
                return True
        return False

    # Delivers package with deadline.
    # First finds the soonest deadline.  Then makes a list of all packages with that deadline.
    # Delivers the packages on that list and loops until all packages with deadlines are delivered.
    # Time = (O)n2
    # Space = (O)n
    def deliverdeadline(self):
        soonestlist = []
        soonest = None
        # Sets a variable equal to a random item with a deadline other than EOD
        for item in self.items:
            if item.deadline != "EOD":
                soonest = item
                break
        # Finds the soonest deadline
        for item in self.items:
            if "EOD" not in item.deadline and Package.gettimedelta(item.deadline) <= Package.gettimedelta(soonest.deadline):
                soonest = item
        # Creates a list of packages with deadlines equal to the soonest deadline
        if soonest is not None:
            for item in self.items:
                if item.deadline == soonest.deadline and item is not soonest:
                    soonestlist.append(item)

            soonestlist.append(soonest)
            nextpackage = Distance.getclosestpackagebyaddress(self.currentlocation, soonestlist)
            self.deliveronepackage(nextpackage)

    # Delivers packages that must be delivered together.
    # Time = (O)n3
    # Space = (O)n
    def delivertogether(self):
        nextpackage = Distance.getclosestpackagebyaddress(self.currentlocation, self.removeunknownaddress(self.mustdelivertogetherlist))
        self.mustdelivertogetherlist.remove(nextpackage)
        self.deliveronepackage(nextpackage)

    # Delivers the package on the truck with the lowest travel distance from the truck's current location.
    # Time = (O)n3
    # Space = (O)n
    def deliverany(self):
        nextpackage = Distance.getclosestpackagebyaddress(self.currentlocation, self.removeunknownaddress(self.items))
        self.deliveronepackage(nextpackage)

    # Returns true if late packages have arrived at the hub.
    # Else false.
    # Time = (O)1
    # Space = (O)n
    def checkiflatepackagearrived(self):
        if len(self.removedelays(Truck.getremainingpackages())) == len(Truck.getremainingpackages()):
            return True
        else:
            return False

    # This mimics the truck waiting for the correct address information if it
    # has no other work to do.
    # Time = (O)n3
    # Space = (O)n
    def updateaddresses(self):
        if len(Truck.getremainingpackages()) == 0:
            if len(self.removeunknownaddress(self.items)) == 0:
                if len(self.items) != 0:
                    itemwithsoonestupdate = self.items[0]
                    for package in self.items:
                        if package.timeavailable < itemwithsoonestupdate.timeavailable:
                            itemwithsoonestupdate = package
                    self.currenttimeunknownaddress = itemwithsoonestupdate.timeavailable

    # Master delivery method that calls all other delivery method.
    # Delivers one package at a time.
    # Time = (O)n3
    # Space = (O)n
    def delivernextpackage(self):
        self.updateaddresses()

        if self.checkiflatepackagearrived() and len(self.items) < 9 and Truck.checkifdelaysremain() \
                and len(self.mustdelivertogetherlist) == 0:
            self.returntowgu()
            self.loadtruck()

        elif len(self.mustdelivertogetherlist) != 0:
            self.delivertogether()

        elif len(self.removeunknownaddress(self.items)) != 0:
            if self.checkifdeadlines():
                self.deliverdeadline()
            else:
                self.deliverany()

        elif len(Truck.getremainingpackages()) != 0:
            self.returntowgu()
            self.loadtruck()

    # Returns the truck to WGU
    # Time = (O)n
    # Space = (O)n
    def returntowgu(self):
        distancetowgu = Distance.getdistancebetweenbyaddress(self.currentlocation, "Western Governors University")
        self.distancetravelled = self.distancetravelled + Decimal(distancetowgu)
        self.currentlocation = "Western Governors University"