import random
from maplist import maplist
from map import map

class ban:

    def __init__(self, id, game, user1, user2, bestof):
        self.id = id
        self.game = game
        self.user1 = user1
        self.user2 = user2
        self.bestof = bestof
        self.nextBan = ""
        self.banNum = 0
        self.history = ""
        self.allmaps = maplist(self.game)
    
    def getUID(self):
        UID = [self.user1ID, self.user2ID]
        return UID

    def setUID(self, user, value):
        if user == 1:
            self.user1ID = value
        elif user == 2:
            self.user2ID = value


    def getId(self):
        return self.id


    def setId(self, id):
        self.id = id

    def getUsers(self):
        return [self.user1, self.user2]


    def setUsers(self, user1, user2):
        self.user1 = user1
        self.user2 = user2

    def getAllmaps(self):
        return self.allmaps

    def getBestof(self):
        return self.bestof

    def setBestof(self, bestof):
        self.bestof = bestof

    def getUnbannedmaps(self):
        return self.allmaps.checkUnbannedMaps()


    def startbans(self):
        retstring = ""
        team1 = random.randrange(2)
        if self.bestof is 1:
            retstring = "Maps in pool are:\n"
            for x in self.allmaps.getMaps():
                retstring+= x.getName()
                retstring+="\n"
            retstring+= "\nBest of 1, each team bans till the last map remaining."
            if team1 == 0:
                retstring+= "\n" + str(self.user1) + " has been randomly picked to start bans."
                self.nextBan = self.user1ID
            if team1 == 1:
                retstring+=" \n" + str(self.user2) + " has been randomly picked to start bans."
                self.nextBan = self.user2ID
        elif self.bestof is 3:
            retstring = "Maps in pool are:\n"
            for x in self.allmaps.getMaps():
                retstring+= x.getName()
                retstring+="\n"
            retstring+= "\nBest of 3, each team bans twice, picks once, bans once."
            if team1 == 0:
                retstring+="\n" + str(self.user1) + " has been randomly picked to start bans."
                self.nextBan = self.user1ID
            if team1 == 1:
                retstring+="\n" + str(self.user2) + " has been randomly picked to start bans."
                self.nextBan = self.user2ID

        return retstring

    def processBan(self):
        retstring = self.getUnbannedmaps()
        if self.bestof is 1:
            retstring += "\nIt is your turn to ban, react to ban the next map"
        if self.bestof is 3:
            banstage = [0, 1, 2, 3, 6, 7]
            pickstage = [4, 5]
            if self.banNum in banstage:
                retstring += "\nIt is your turn to ban, react to ban the next map"
            elif self.banNum in pickstage:
                retstring += "\nIt is your turn to pick, react to pick the next map"
        return retstring

    def checkMaps(self):
        i = 0
        for m in self.allmaps.getMaps():
            if m == "Neutral":
                i+= 1
        return i

    def getnextBan(self):
        return self.nextBan

    def banpick(self, mapnum):
        print("ban num before" + str(self.banNum))
        msg = ""
        maplist = []
        currBan = ""
        if self.nextBan == self.user1ID:
            currBan = self.user1
        elif self.nextBan == self.user2ID:
            currBan = self.user2
        for m in self.allmaps.getMaps():
            if m.checkCondition() == "Neutral":
                maplist.append(m.getName())
        if self.bestof == 1:
            maps = self.allmaps.getMaps()
            for m in maps:
                if m.getName() == maplist[mapnum]:
                    m.banMap()        
            msg = currBan + " banned " + maplist[mapnum]
            self.history += msg + "\n"
        if self.bestof == 3:
            banstage = [0, 1, 2, 3, 6, 7]
            if self.banNum in banstage:
                self.allmaps[maplist[mapnum]] = "Banned"
                msg = currBan + " Banned " + maplist[mapnum]
                self.history += msg + "\n"
            elif self.banNum == 4:
                self.allmaps[maplist[mapnum]] = "picked1"
                msg = currBan + " picked " + maplist[mapnum]
                self.history += msg + "\n"
            elif self.banNum == 5:
                self.allmaps[maplist[mapnum]] = "picked2"
                msg = currBan + " picked " + maplist[mapnum]
                self.history += msg + "\n"                  
        if self.nextBan == self.user1ID:
            self.nextBan = self.user2ID
        elif self.nextBan == self.user2ID:
            self.nextBan = self.user1ID
        self.banNum += 1
        return msg

    def getRemainingMaps(self):
        retstring = "Final map(s) are:\n"
        if self.bestof == 1:
            retstring += self.findMaps("Neutral")
        if self.bestof == 3:
            retstring += self.findMaps("picked1") + "\n"
            retstring += self.findMaps("picked2") + "\n"
            retstring += self.findMaps("Neutral") + "\n"
        print(retstring)
        return retstring

    def findMaps(self, term):
        for m in self.allmaps.getMaps():
            if m.checkCondition() is term:
                return m.getName()

    def getHistory(self):
        return self.history