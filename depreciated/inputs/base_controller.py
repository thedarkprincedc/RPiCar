class BaseController:
    def __init__(self, device):
        self.device = device
        self.id = None
    def read(self):
        raise NotImplementedError
    def parse(self):
        raise NotImplementedError

