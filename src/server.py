from aiohttp import web
from web.routes.camera import routes as camera_routes
from web.routes.controls import routes as control_routes
from web.routes.telemetry import routes as telemetry_routes
from pathlib import Path
from web.camera import Camera
import logging
from logging_config import setup_logging
import argparse
from config import AppConfig

logger = logging.getLogger(__name__)

def create_app(debug=None):
    if debug is None:
        debug = AppConfig.DEBUG

    setup_logging(
        log_file="logs/server.log", 
        console_level=logging.DEBUG if debug else logging.INFO,
        log_to_file=True
    )

    logger.info(f"debug mode: {debug}")

    app = web.Application()
    app["config"] = AppConfig
    
    app["camera"] = Camera(
        device=0,
        width=1920,
        height=1080,
        fps=60
    )

    app.router.add_static("/static/",  app["config"].RPI_STATIC_DIR)
    app.add_routes(camera_routes)
    app.add_routes(control_routes)
    app.add_routes(telemetry_routes)

    return app

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    args = parser.parse_args()

    app = create_app(args.debug)

    web.run_app(
        app,
        host="0.0.0.0",
        port=AppConfig.RPI_PORT,
        access_log=logging.getLogger("aiohttp.access"),
        access_log_format='%a "%r" %s %b "%{User-Agent}i"'
    )

if __name__ == "__main__":
    main()