from inputs.base_controller import BaseController

class XboxController(BaseController):
    def read(self):
        data = self.device.read(64)
        if not data:
            return None
        return self.parse(data)

    def parse(self):
        raise NotImplementedError