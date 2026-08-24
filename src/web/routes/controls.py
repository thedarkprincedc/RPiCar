import json
import logging
from aiohttp import web, WSMsgType

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)


routes = web.RouteTableDef()

# All currently connected WebSocket clients
connected_clients = set()

async def broadcast(message):
    """
    Send a message to every connected WebSocket client.
    """

    # Make a copy because clients can disconnect while we're iterating
    for ws in connected_clients.copy():

        if ws.closed:
            connected_clients.discard(ws)
            continue

        try:
            await ws.send_str(message)

        except Exception:
            logger.exception("Failed to send message to WebSocket client")
            connected_clients.discard(ws)

@routes.get("/ws/control")
async def control_websocket(request):
    ws = web.WebSocketResponse()

    await ws.prepare(request)

    connected_clients.add(ws)
    
    logger.info(
        "WebSocket client connected (%d clients)",
        len(connected_clients)
    )

    try:
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:

                logger.info(
                    "Received from client: %s",
                    msg.data
                )

                # Validate that the message is JSON
                try:
                    data = json.loads(msg.data)
                except json.JSONDecodeError:
                    logger.warning(
                        "Received invalid JSON: %s",
                        msg.data
                    )
                    continue

                # Broadcast to all clients
                await broadcast(
                    json.dumps(data)
                )
            elif msg.type == WSMsgType.ERROR:

                logger.error(
                    "WebSocket error: %s",
                    ws.exception()
                )
    finally:
        connected_clients.discard(ws)

        logger.info(
            "WebSocket client disconnected (%d clients)",
            len(connected_clients)
        )
    
    return ws
    