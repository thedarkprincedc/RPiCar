import json
from aiohttp import ClientSession, WSMsgType, ClientConnectorError 

class TelemetryPublisher():
    def __init__(self, url = "ws://localhost:5000/ws/control"):
        self.url = url
        self.session = None
        self.ws = None

    async def connect(self):
        self.session = ClientSession()
        self.ws = await self.session.ws_connect(self.url)

    async def publish(self, data):
        if self.ws is None:
            return
        await self.ws.send_str(json.dumps(data))

    async def close(self):
        if self.ws:
            await self.ws.close()
        if self.session:
            await self.session.close()
