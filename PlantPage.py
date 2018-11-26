class PlantPage(object):
    __slots__ = ['name', 'link', 'data', 'text', 'references']
    def __init__(self, name):
        self.name = name
        self.data = dict()

    def get_name(self):
        return self.name

    def add_heading(self, h3):
        self.data[h3] = list()

    def add_div(self, h3, div):
        self.data[h3] += [div]

    def get_data(self):
        return self.data

    def set_link(self, url):
        self.link = url

    def get_link(self):
        return self.link

    def set_text(self, text):
        self.text = text

    def get_text(self):
        return self.text

    def set_references(self, urls):
        self.references = urls

    def get_references(self):
        return self.references
