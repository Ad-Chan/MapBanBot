import random

class valorant:

    def __init__(self, id, user1, user2, bestof):
        self.id = id
        self.user1 = user1
        self.user2 = user2
        self.user1ID = ""
        self.user2ID = ""
        self.allmaps = {"Ascent":"neutral", "Bind":"neutral", "Haven":"neutral", "Split":"neutral", "Icebox":"neutral", "Breeze":"neutral"}
        self.bestof = bestof
        self.nextBan = ""
        self.banNum = 0
        self.history = ""

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
        #team1 = random.randrange(2)
        if self.bestof == 1:
            retstring = "Maps in pool are:\n"
            for x in self.allmaps:
                retstring+= x
                retstring+="\n"
            retstring+= "\nBest of 1, each team bans till the last map remaining."


        elif self.bestof == 3:
            retstring = "Maps in pool are:\n"
            for x in self.allmaps:
                retstring+= x
                retstring+="\n"
            retstring+= "\nBest of 3, each team bans once, picks once, bans once."
        
        self.nextBan = self.user1ID
        return retstring

    def processBan(self):
        retstring = self.getUnbannedmaps()
        if self.bestof == 1:
            retstring += "\nIt is your turn to ban, react to ban the next map"
        if self.bestof == 3:
            banstage = [0, 1]
            pickstage = [2, 3]
            if self.banNum in banstage:
                retstring += "\nIt is your turn to ban, react to ban the next map"
            elif self.banNum in pickstage:
                retstring += "\nIt is your turn to pick, react to pick the next map"
        return retstring


    def checkMaps(self):
        i = 0
        for x, y in self.allmaps.items():
            if y == "neutral":
                i+= 1
        #print("checkMaps " + str(i))
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
        currBan = ""
        if self.nextBan == self.user1ID:
            currBan = self.user1
        elif self.nextBan == self.user2ID:
            currBan = self.user2
        for x, y in self.allmaps.items():
            if y == "neutral":
                maplist.append(x)
        print(maplist)
        if self.bestof == 1:
            self.allmaps[maplist[mapnum]] = "banned"
            msg = currBan + " banned " + maplist[mapnum]
            self.history += msg + "\n"
        if self.bestof == 3:
            banstage = [0, 1]
            if self.banNum in banstage:
                self.allmaps[maplist[mapnum]] = "banned"
                msg = currBan + " banned " + maplist[mapnum]
                self.history += msg + "\n"
            elif self.banNum == 2:
                self.allmaps[maplist[mapnum]] = "picked1"
                msg = currBan + " picked " + maplist[mapnum]
                self.history += msg + "\n"
            elif self.banNum == 3:
                self.allmaps[maplist[mapnum]] = "picked2"
                msg = currBan + " picked " + maplist[mapnum]
                self.history += msg + "\n"                      
        if self.nextBan == self.user1ID:
            self.nextBan = self.user2ID
        elif self.nextBan == self.user2ID:
            self.nextBan = self.user1ID
        self.banNum += 1
        print("ban num after" + str(self.banNum))
        print(self.allmaps)
        return msg

    def getRemainingMaps(self):
        print(self.allmaps)
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
            if y == term:
                return x

    def getHistory(self):
        return self.history

    def randBan(self):
        num = random.randrange(2)
        unbanned = []
        msg = ""
        for x, y in self.allmaps.items():
            if y == "neutral":
                unbanned.append(x)
        if num == 0:
            self.allmaps[unbanned[0]] = 'banned'
            msg += "Randomiser has banned " + unbanned[0] + "\n"
        elif num == 1:
            self.allmaps[unbanned[1]] = 'banned'
            msg += "Randomiser has banned " + unbanned[1] + "\n"
        self.history += msg
