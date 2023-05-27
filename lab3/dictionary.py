import bisect
import pickle

class Dictionary:
    def __init__(self):
        self.data = self.load()

    def translate(self, key):
        if(key in self.data):
            return self.data[key]
        return []

    def add(self, key, value):
        new = False
        if(key not in self.data):
            self.data[key] = []
            new = True
        bisect.insort(self.data[key], value)
        return new

    def delete(self, key):
        del self.data[key]

    def load(self):
        try:
            with open('dict.bin', 'rb') as f:
                data = pickle.load(f)
                return data
        except:
            return {}

    def save(self):
        with open('dict.bin', 'wb') as f:
            pickle.dump(self.data, f)

