from inputs.base_controller import BaseController

class XboxController(BaseController):
    def __init__(self, device, transport="usb"):
        self.device = device
        self.transport = transport
        
    def read(self):
        data = self.device.read(64)
        if not data:
            return None
        return self.parse(data)

    def parse(self):
        raise NotImplementedError