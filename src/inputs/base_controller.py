from abc import ABC, abstractmethod
#from controller_state import ControllerState

class BaseController(ABC):

    def __init__(self):
        self._state = {}

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass