from inputs.base_controller import BaseController
from inputs.controller_state import ControllerState
from aiohttp import ClientSession, WSMsgType, ClientConnectorError 
import threading
import asyncio
import json
import copy
import logging

logger = logging.getLogger("websocket_controller")

class WebSocketController(BaseController):
    def __init__(self):
        super().__init__()
        self.url = "ws://localhost:5000/ws/control"
        self.transport = "websocket"
        self.thread = None
        self.connected = False
        self.stop_event = threading.Event()
        self.connected_event = threading.Event()
        self._state = ControllerState()

    def connect(self):
        try: 
            #logger.info("WebSocketController connected")
            self.thread = threading.Thread(
                target=self._run,
                daemon=True
            )
            self.thread.start()
            self.connected_event.wait(timeout=5)
            return self.connected_event.is_set()
        
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
        controllers.append(
            cls()
        )
        return controllers

    def _run(self):
        asyncio.run(self._connect())

    # async def _connect(self):
    #     async with ClientSession() as session:
    #         async with session.ws_connect(self.url) as ws:
    #             self.connected = True
    #             logger.info(
    #                 "WebSocket connected"
    #             )

    #             try:
    #                 async for message in ws:
    #                     if message.type == WSMsgType.TEXT:
    #                         self._handle_message(message.data)

    #                     elif message.type == WSMsgType.ERROR:
    #                         print(ws.exception())

    #             finally:
    #                 self.connected = False
    #                 self.reset()
    #                 logger.info(
    #                     "WebSocket disconnected"
    #                 )

    async def _connect(self):
        try:
            async with ClientSession() as session:
                async with session.ws_connect(self.url) as ws:
                   
                    self.connected = True
                    self.connected_event.set()
                    
                    logger.info("WebSocket connected: %s", self.url)

                    async for message in ws:
                        await self._handle_message(message.data)

        except ClientConnectorError as e:
            self.connected = False
            logger.warning("WebSocket connection failed: %s", e)
        except Exception:
            self.connected = False
            logger.exception("WebSocket error")

    async def _handle_message(self, data):
        data = json.loads(data)
        logger.info(data)
        self._state.update(data)