class SerialDriver:
    def write(self, data):
        raise NotImplementedError

    def close(self):
        pass

    def get_battery(self):
        pass