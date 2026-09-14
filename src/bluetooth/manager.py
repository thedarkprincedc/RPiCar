import asyncio
from dataclasses import dataclass, field
from typing import Any

from dbus_next import BusType, Variant
from dbus_next.aio import MessageBus
from dbus_next.message import Message
from dbus_next.service import ServiceInterface, method
from dbus_next.constants import MessageType


BLUEZ_SERVICE = "org.bluez"
ADAPTER = "/org/bluez/hci0"

DEVICE_INTERFACE = "org.bluez.Device1"
ADAPTER_INTERFACE = "org.bluez.Adapter1"
AGENT_INTERFACE = "org.bluez.Agent1"
AGENT_MANAGER_INTERFACE = "org.bluez.AgentManager1"
OBJECT_MANAGER_INTERFACE = "org.freedesktop.DBus.ObjectManager"

AGENT_PATH = "/com/rpicar/bluetooth/agent"


@dataclass
class BluetoothDevice:
    path: str
    name: str
    address: str
    alias: str | None = None
    paired: bool = False
    connected: bool = False
    trusted: bool = False
    uuids: list[str] = field(default_factory=list)
    device_class: int | None = None

    def to_dict(self):
        return {
            "path": self.path,
            "name": self.name,
            "address": self.address,
            "alias": self.alias,
            "paired": self.paired,
            "connected": self.connected,
            "trusted": self.trusted,
            "uuids": self.uuids,
            "class": self.device_class,
        }


class PairingAgent(ServiceInterface):
    """
    BlueZ pairing agent.

    NoInputNoOutput works well for controllers that use
    Just Works pairing.
    """

    def __init__(self):
        super().__init__(AGENT_INTERFACE)

    @method()
    def Release(self):
        pass

    @method()
    def RequestPinCode(self, device: "o") -> "s":
        return "0000"

    @method()
    def DisplayPinCode(
        self,
        device: "o",
        pincode: "s",
    ):
        print(f"Bluetooth PIN: {pincode}")

    @method()
    def RequestPasskey(self, device: "o") -> "u":
        return 0

    @method()
    def DisplayPasskey(
        self,
        device: "o",
        passkey: "u",
        entered: "q",
    ):
        print(
            f"Bluetooth passkey: "
            f"{passkey:06d}"
        )

    @method()
    def RequestConfirmation(
        self,
        device: "o",
        passkey: "u",
    ):
        print(
            f"Bluetooth confirmation "
            f"requested: {passkey:06d}"
        )

    @method()
    def RequestAuthorization(
        self,
        device: "o",
    ):
        print(
            f"Bluetooth authorization requested: "
            f"{device}"
        )

    @method()
    def AuthorizeService(
        self,
        device: "o",
        uuid: "s",
    ):
        print(
            f"Bluetooth service authorization: "
            f"{uuid}"
        )

    @method()
    def Cancel(self):
        print("Bluetooth pairing cancelled")


class BluetoothManager:

    def __init__(
        self,
        adapter: str = ADAPTER,
    ):
        self.adapter = adapter
        self.bus: MessageBus | None = None

        self.devices: dict[
            str,
            BluetoothDevice
        ] = {}

        self.agent = PairingAgent()

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    @staticmethod
    def unwrap(
        value: Any,
        default=None,
    ):
        if value is None:
            return default

        if isinstance(value, Variant):
            return value.value

        if hasattr(value, "value"):
            return value.value

        return value

    # ---------------------------------------------------------
    # Connection
    # ---------------------------------------------------------

    async def connect_bus(self):

        if self.bus:
            return

        self.bus = await MessageBus(
            bus_type=BusType.SYSTEM
        ).connect()

        self.bus.add_message_handler(
            self._message_handler
        )

    # ---------------------------------------------------------
    # D-Bus events
    # ---------------------------------------------------------

    def _message_handler(self, message):

        if message.message_type != MessageType.SIGNAL:
            return

        if (
            message.interface
            != OBJECT_MANAGER_INTERFACE
        ):
            return

        if message.member == "InterfacesAdded":

            path, interfaces = message.body

            properties = interfaces.get(
                DEVICE_INTERFACE
            )

            if properties:
                device = self._parse_device(
                    path,
                    properties,
                )

                self.devices[path] = device

                print(
                    f"Bluetooth device found: "
                    f"{device.name} "
                    f"{device.address}"
                )

        elif message.member == "InterfacesRemoved":

            path, interfaces = message.body

            if DEVICE_INTERFACE in interfaces:
                self.devices.pop(
                    path,
                    None,
                )

    # ---------------------------------------------------------
    # Device parsing
    # ---------------------------------------------------------

    def _parse_device(
        self,
        path: str,
        properties: dict,
    ) -> BluetoothDevice:

        return BluetoothDevice(
            path=path,

            name=self.unwrap(
                properties.get("Name"),
                "<unknown>",
            ),

            address=self.unwrap(
                properties.get("Address"),
                "<unknown>",
            ),

            alias=self.unwrap(
                properties.get("Alias"),
            ),

            paired=self.unwrap(
                properties.get("Paired"),
                False,
            ),

            connected=self.unwrap(
                properties.get("Connected"),
                False,
            ),

            trusted=self.unwrap(
                properties.get("Trusted"),
                False,
            ),

            uuids=self.unwrap(
                properties.get("UUIDs"),
                [],
            ),

            device_class=self.unwrap(
                properties.get("Class"),
            ),
        )

    # ---------------------------------------------------------
    # Existing devices
    # ---------------------------------------------------------

    async def refresh_devices(self):

        await self.connect_bus()

        reply = await self.bus.call(
            Message(
                destination=BLUEZ_SERVICE,
                path="/",
                interface=OBJECT_MANAGER_INTERFACE,
                member="GetManagedObjects",
            )
        )

        objects = reply.body[0]

        for path, interfaces in objects.items():

            properties = interfaces.get(
                DEVICE_INTERFACE
            )

            if not properties:
                continue

            device = self._parse_device(
                path,
                properties,
            )

            self.devices[path] = device

        return list(
            self.devices.values()
        )

    # ---------------------------------------------------------
    # Discovery
    # ---------------------------------------------------------

    async def start_discovery(self):

        await self.connect_bus()

        await self.bus.call(
            Message(
                destination=BLUEZ_SERVICE,
                path=self.adapter,
                interface=ADAPTER_INTERFACE,
                member="StartDiscovery",
            )
        )

    async def stop_discovery(self):

        if not self.bus:
            return

        try:

            await self.bus.call(
                Message(
                    destination=BLUEZ_SERVICE,
                    path=self.adapter,
                    interface=ADAPTER_INTERFACE,
                    member="StopDiscovery",
                )
            )

        except Exception:
            pass

    async def scan(
        self,
        timeout: float = 10,
    ):

        await self.connect_bus()

        await self.refresh_devices()

        await self.start_discovery()

        try:
            await asyncio.sleep(timeout)

        finally:
            await self.stop_discovery()

        return list(
            self.devices.values()
        )

    # ---------------------------------------------------------
    # Device lookup
    # ---------------------------------------------------------

    async def get_device(
        self,
        address: str,
    ) -> BluetoothDevice | None:

        await self.refresh_devices()

        address = address.upper()

        for device in self.devices.values():

            if device.address.upper() == address:
                return device

        return None

    # ---------------------------------------------------------
    # Pairing agent
    # ---------------------------------------------------------

    async def register_agent(self):

        await self.connect_bus()

        self.bus.export(
            AGENT_PATH,
            self.agent,
        )

        await self.bus.call(
            Message(
                destination=BLUEZ_SERVICE,
                path="/org/bluez",
                interface=AGENT_MANAGER_INTERFACE,
                member="RegisterAgent",
                signature="osa{sv}",
                body=[
                    AGENT_PATH,
                    "NoInputNoOutput",
                    {},
                ],
            )
        )

        await self.bus.call(
            Message(
                destination=BLUEZ_SERVICE,
                path="/org/bluez",
                interface=AGENT_MANAGER_INTERFACE,
                member="RequestDefaultAgent",
                signature="o",
                body=[
                    AGENT_PATH,
                ],
            )
        )

        print("Bluetooth pairing agent registered")

    # ---------------------------------------------------------
    # Pair
    # ---------------------------------------------------------

    async def pair(
        self,
        address: str,
    ):

        device = await self.get_device(
            address
        )

        if not device:
            raise RuntimeError(
                f"Bluetooth device not found: "
                f"{address}"
            )

        print(
            f"Pairing with "
            f"{device.name} "
            f"{device.address}"
        )

        reply = await self.bus.call(
            Message(
                destination=BLUEZ_SERVICE,
                path=device.path,
                interface=DEVICE_INTERFACE,
                member="Pair",
            )
        )

        if reply.error_name:
            raise RuntimeError(
                f"Pair failed: "
                f"{reply.error_name}"
            )

        await self.refresh_devices()

        return await self.get_device(
            address
        )

    # ---------------------------------------------------------
    # Connect
    # ---------------------------------------------------------

    async def connect(
        self,
        address: str,
    ):

        device = await self.get_device(
            address
        )

        if not device:
            raise RuntimeError(
                f"Bluetooth device not found: "
                f"{address}"
            )

        print(
            f"Connecting to "
            f"{device.name} "
            f"{device.address}"
        )

        reply = await self.bus.call(
            Message(
                destination=BLUEZ_SERVICE,
                path=device.path,
                interface=DEVICE_INTERFACE,
                member="Connect",
            )
        )

        if reply.error_name:
            raise RuntimeError(
                f"Connect failed: "
                f"{reply.error_name}"
            )

        await self.refresh_devices()

        return await self.get_device(
            address
        )

    # ---------------------------------------------------------
    # Disconnect
    # ---------------------------------------------------------

    async def disconnect(
        self,
        address: str,
    ):

        device = await self.get_device(
            address
        )

        if not device:
            raise RuntimeError(
                f"Bluetooth device not found: "
                f"{address}"
            )

        reply = await self.bus.call(
            Message(
                destination=BLUEZ_SERVICE,
                path=device.path,
                interface=DEVICE_INTERFACE,
                member="Disconnect",
            )
        )

        if reply.error_name:
            raise RuntimeError(
                f"Disconnect failed: "
                f"{reply.error_name}"
            )

        await self.refresh_devices()

    # ---------------------------------------------------------
    # Remove
    # ---------------------------------------------------------

    async def remove(
        self,
        address: str,
    ):

        device = await self.get_device(
            address
        )

        if not device:
            raise RuntimeError(
                f"Bluetooth device not found: "
                f"{address}"
            )

        reply = await self.bus.call(
            Message(
                destination=BLUEZ_SERVICE,
                path=self.adapter,
                interface=ADAPTER_INTERFACE,
                member="RemoveDevice",
                signature="o",
                body=[
                    device.path,
                ],
            )
        )

        if reply.error_name:
            raise RuntimeError(
                f"Remove failed: "
                f"{reply.error_name}"
            )

        self.devices.pop(
            device.path,
            None,
        )

    # ---------------------------------------------------------
    # Shutdown
    # ---------------------------------------------------------

    async def close(self):

        if not self.bus:
            return

        await self.stop_discovery()

        self.bus.disconnect()
        self.bus = None


# =============================================================
# Test
# =============================================================

async def main():

    bluetooth = BluetoothManager()

    try:

        await bluetooth.register_agent()

        print("\nScanning...\n")

        devices = await bluetooth.scan(
            timeout=10
        )

        for device in devices:

            print(
                f"{device.name:40} "
                f"{device.address:17} "
                f"paired={device.paired} "
                f"connected={device.connected}"
            )

    finally:

        await bluetooth.close()


if __name__ == "__main__":
    asyncio.run(main())