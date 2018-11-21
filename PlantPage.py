class PlantPage(object):
    __slots__ = ['name', 'link', 'data']
    def __init__(self, name):
        self.name = name
        self.data = dict()

    def add_heading(self, h3):
        self.data[h3] = list()

    def add_div(self, h3, div):
        self.data[h3] += [div]

    def set_link(self, url):
        self.link = url
