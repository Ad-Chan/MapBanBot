import random

class cs:

    def __init__(self, id, user1, user2, bestof):
        self.id = id
        self.user1 = user1
        self.user2 = user2
        self.allmaps = {"de_dust2":"neutral", "de_inferno":"neutral", "de_mirage":"neutral", "de_nuke":"neutral", 
        "de_overpass":"neutral", "de_train":"neutral", "de_vertigo":"neutral"}
        #use "neutral" OR "banned" OR "picked"
        #self.playmaps = []
        self.bestof = bestof
        self.nextBan = ""
        self.banNum = 0
        self.history = ""

    
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
        reaction = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣']
        retstring = "Maps remaining:"
        i = 0
        for x, y in self.allmaps.items():
            if y == "neutral":
                retstring+= "\n"
                retstring+= reaction[i]
                retstring+= " for "
                retstring+= str(x)
                i+=1
        return retstring

    def startbans(self):
        retstring = ""
        team1 = random.randrange(2)
        if self.bestof is 1:
            retstring = "Maps in pool are:\n"
            for x in self.allmaps:
                retstring+= x
                retstring+="\n"
            retstring+= "\nBest of 1, each team bans till the last map remaining."
            if team1 == 0:
                retstring+= "\n" + str(self.user1) + " has been randomly picked to start bans."
                self.nextBan = self.user1
            if team1 == 1:
                retstring+=" \n" + str(self.user2) + " has been randomly picked to start bans."
                self.nextBan = self.user2

        elif self.bestof is 3:
            retstring = "Maps in pool are:\n"
            for x in self.allmaps:
                retstring+= x
                retstring+="\n"
            retstring+= "\nBest of 3, each team bans once, picks once, bans once."
            if team1 == 0:
                retstring+="\n" + str(self.user1) + " has been randomly picked to start bans."
                self.nextBan = self.user1
            if team1 == 1:
                retstring+="\n" + str(self.user2) + " has been randomly picked to start bans."
                self.nextBan = self.user2

        return retstring

    def processBan(self):
        retstring = self.getUnbannedmaps()
        if self.bestof is 1:
            retstring += "\nIt is your turn to ban, react to ban the next map"
        if self.bestof is 3:
            banstage = [0, 1, 4, 5]
            pickstage = [2, 3]
            if self.banNum in banstage:
                retstring += "\nIt is your turn to ban, react to ban the next map"
            elif self.banNum in pickstage:
                retstring += "\nIt is your turn to pick, react to pick the next map"
        return retstring


    def checkMaps(self):
        i = 0
        for x, y in self.allmaps.items():
            if y is "neutral":
                i+= 1
        print("checkMaps " + str(i))
        return i

    def printbans(self):
        print("id: " + str(self.id) + "\n")
        print("users: " + str(self.user1) + " " + str(self.user2) +"\n")
        print("bestof: " + str(self.bestof) + "\n")

    def getnextBan(self):
        return self.nextBan

    def banpick(self, mapnum):
        print("ban num before" + str(self.banNum))
        msg = ""
        maplist = []
        for x, y in self.allmaps.items():
            if y == "neutral":
                maplist.append(x)
        print(maplist)
        if self.bestof == 1:
            self.allmaps[maplist[mapnum]] = "banned"
            msg = self.nextBan + " banned " + maplist[mapnum]
            self.history += msg + "\n"
        if self.bestof == 3:
            banstage = [0, 1, 4, 5]
            if self.banNum in banstage:
                self.allmaps[maplist[mapnum]] = "banned"
                msg = self.nextBan + " banned " + maplist[mapnum]
                self.history += msg + "\n"
            elif self.banNum == 2:
                self.allmaps[maplist[mapnum]] = "picked1"
                msg = self.nextBan + " picked " + maplist[mapnum]
                self.history += msg + "\n"
            elif self.banNum == 3:
                self.allmaps[maplist[mapnum]] = "picked2"
                msg = self.nextBan + " picked " + maplist[mapnum]
                self.history += msg + "\n"                  
        if self.nextBan == self.user1:
            self.nextBan = self.user2
        elif self.nextBan == self.user2:
            self.nextBan = self.user1
        self.banNum += 1
        print("ban num after" + str(self.banNum))
        print(self.allmaps)
        return msg

    def getRemainingMaps(self):
        retstring = "Final map(s) are:\n"
        if self.bestof == 1:
            retstring += self.findMaps("neutral")
        if self.bestof == 3:
            retstring += self.findMaps("picked1") + "\n"
            retstring += self.findMaps("picked2") + "\n"
            retstring += self.findMaps("neutral") + "\n"
        print(retstring)
        return retstring

    def findMaps(self, term):
        for x, y in self.allmaps.items():
            if y is term:
                return x

    def getHistory(self):
        return self.history
                

#testclass = cs(1, "u1", "u2", 3)
#print(testclass.startbans())
#print(testclass.getUnbannedmaps())