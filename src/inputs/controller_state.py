from dataclasses import dataclass

@dataclass
class ControllerState():
# analog stocks
    lx: float = 0.0
    ly: float = 0.0
    rx: float = 0.0
    ry: float = 0.0
# analog trigger
    l2: float = 0.0
    r2: float = 0.0
# hat switch
    #dpad: int = 0
# buttons
    # cross: bool = False
    # circle: bool = False
    # square: bool = False
    # triangle: bool = False

    a: bool = False
    b: bool = False
    x: bool = False
    y: bool = False

    l1: bool = False
    r1: bool = False
    l3: bool = False
    r3: bool = False
    options: bool = False
    share: bool = False

    timestamp: float = 0.0