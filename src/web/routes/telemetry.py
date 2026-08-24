import json
from aiohttp import web

routes = web.RouteTableDef()

@routes.get("/ws/telemetry")
async def control_websocket(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            print("Received:", msg.data)

        elif msg.type == web.WSMsgType.ERROR:
            print("WebSocket error:", ws.exception())

    print("Control client disconnected")
    
    return ws