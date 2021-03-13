class map:

    def __init__(self, name, game):
        self.name = name
        self.game = game
        self.condition = "Neutral"
        self.actionedBy = ""

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def banMap(self, captain):
        self.condition = "Banned"
        self.actionedBy = captain

    def pickMap(self, captain):
        self.condition = "Picked"
        self.actionedBy = captain

    def checkCondition(self):
        return self.condition
     