# from aiohttp import web
# from pathlib import Path 

# routes = web.RouteTableDef()

# @routes.get("/api/car/status")
# async def status(request):
#     return web.json_response({
#         "connected": True
#     })

# @routes.get("/api/camera/offer")
# async def offer(request):
#     data = await request.json()
#     return web.json_response({
        
#     })

# # @routes.get("/")
# # async def index(request):
# #     return web.Response(
# #         text=HTML,
# #         content_type="text/html" 
# #     )

# @routes.get("/")
# async def index(request):
#     TEMPLATES_DIR = Path(__file__).parent / "templates"
#     return web.FileResponse(TEMPLATES_DIR / "index.html")