class PropertyReader:
    def __init__(self, file_name):
        self.file_name = file_name
        self.values = {}
        self.values_temp = []
        self.read_all()

    def read_all(self):
        with open(self.file_name, 'r') as property:
            for temp in property.readlines():
                if not temp.startswith('#'):
                    self.values_temp.append(temp.strip())
        for value in self.values_temp:
            value = value.split('=')
            self.values[value[0]] = value[1]

