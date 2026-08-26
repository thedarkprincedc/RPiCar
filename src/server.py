from aiohttp import web
from web.routes.camera import routes as camera_routes
from web.routes.controls import routes as control_routes
from web.routes.telemetry import routes as telemetry_routes
from pathlib import Path
from web.camera import Camera
import logging
from logging_config import setup_logging
import argparse

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    args = parser.parse_args()

    setup_logging(
        log_file="logs/server.log", 
        console_level=logging.DEBUG if args.debug else logging.INFO
    )

    logger.info("Starting RPiWeb...")
    
    app = web.Application()

    app["camera"] = Camera(
        device=0,
        width=1920,
        height=1080,
        fps=60
    )

    app["templates"] = BASE_DIR / "web/templates"

    app.router.add_static(
        "/static/",
        BASE_DIR / "web/static"
    )

    app.add_routes(camera_routes)
    app.add_routes(control_routes)
    app.add_routes(telemetry_routes)

    print("Open http://localhost:5000")

    web.run_app(
        app,
        host="0.0.0.0",
        port=5000,
        access_log=logging.getLogger("aiohttp.access"),
        access_log_format='%a "%r" %s %b "%{User-Agent}i"'
    )

if __name__ == "__main__":
    main()