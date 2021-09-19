class PropertyReader:
    def __init__(self, file_name):
        self.fileName = file_name
        self.values = {}
        self.values_temp = []
        self.read_all()

    def read_all(self):
        with open(self.fileName, 'r') as property:
            for temp in property.readlines():
                if not temp.startswith('#'):
                    self.values_temp.append(temp.strip())
        for value in self.values_temp:
            value = value.split('=')
            self.values[value[0]] = value[1]

    def set_key(self, key, value):
        self.read_all()
        self.values[key] = value

    def save(self):
        with open(self.fileName, mode='w') as property:
            for temp in self.values:
                property.write(f'{temp}={self.values[temp]}\n')

    def __str__(self):
        return self.values