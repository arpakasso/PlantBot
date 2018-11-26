class User(object):
    __slots__ = ['zone']

    def __init__(self):
        self.zone = ""

    def set_zone(self, zone):
        self.zone = zone

    def get_zone(self):
        return self.zone