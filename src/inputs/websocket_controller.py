from inputs.base_controller import BaseController
from inputs.controller_state import ControllerState
from aiohttp import ClientSession, WSMsgType
import threading
import asyncio
import json
import copy
import logging

logger = logging.getLogger(__name__)

class WebSocketController(BaseController):
    def __init__(self, url, transport = "websocket"):
        super().__init__()

        self.url = url
        self._state = ControllerState()

        self.thread = None
        self.stop_event = threading.Event

    def connect(self):
        try: 
            logger.info("WebSocketController connected")

            self.thread = threading.Thread(
                target=self._run,
                daemon=True
            )

            self.thread.start()

            return True
        except Exception as e:
            logger.info(f"WebSocketController connection failed: {e}")
            return False

    def disconnect(self):
        self.stop_event.set()

    def update(self):
        self._state = self.parse()
        return self._state

    def parse(self):
        return {
            "lx": 0,
            "ly": 0
        }
    
    def get_state(self):
            return copy.copy(self._state)
    
    @classmethod
    def scan(cls):
        controllers = []
        transport = "websocket"
        url = "ws://localhost:5000/ws/control"
        controllers.append(
            cls(url,transport)
        )
        return controllers

    def _run(self):
        asyncio.run(self._connect())

    async def _connect(self):
        async with ClientSession() as session:
            async with session.ws_connect(self.url) as ws:
                self.connected = True
                logger.info(
                    "WebSocket connected"
                )

                try:
                    async for message in ws:
                        if message.type == WSMsgType.TEXT:
                            self._handle_message(message.data)

                        elif message.type == WSMsgType.ERROR:
                            print(ws.exception())

                finally:
                    self.connected = False
                    self.reset()
                    logger.info(
                        "WebSocket disconnected"
                    )

    def _handle_message(self, data):
        data = json.loads(data)
        print(data)

        self._state.update(data)