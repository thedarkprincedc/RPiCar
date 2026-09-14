class BaseSerialDriver:
    def write(self, data):
        raise NotImplementedError

    def close(self):
        pass

    def read_json(self):
        pass