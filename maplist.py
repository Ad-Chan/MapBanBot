from map import map

class maplist:

    def __init__(self, game):
        self.game = game
        self.maps = []
        self.setMapList()

    def getGame(self):
        return self.game
    
    def setGame(self, game):
        self.game = game

    def setMapList(self):
        if self.game == "csgo":
            csgomaps = self.setMaps("csgo_maps")
            for mapname in csgomaps:
                newmap = map(mapname, "csgo")
                self.maps.append(newmap)

        elif self.game == "r6":
            r6maps = self.setMaps("r6_maps")
            for mapname in r6maps:
                newmap = map(mapname, "r6")
                self.maps.append(newmap)
        elif self.game == "val":
            valmaps = self.setMaps("val_maps")
            for mapname in valmaps:
                newmap = map(mapname, "val")
                self.maps.append(newmap)

    def setMaps(self, game):
        maplist = []
        path = "Maps/" + game
        file = open(path, 'r')
        for m in file:
            maplist.append(m)
        file.close()
        return maplist

    def checkUnbannedMaps(self):
        reaction = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
        retstring = "Maps remaining:"
        i = 0
        for m in self.maps:
            if m.checkCondition() == "Neutral":
                retstring+= "\n"
                retstring+= reaction[i]
                retstring+= " for "
                retstring+= str(m.getName())
                i+=1
        return retstring
    
    def getMaps(self):
        return self.maps