import rio
from ..utils.logging import get_logger
from ..web.dashboard import Dashboard

log = get_logger(__name__)

# This file defines the Rio app. It is intended to be run with the `rio` CLI.
app = rio.App(
    build=Dashboard,
    # You can add assets here later, e.g., assets_dir="path/to/assets"
)

log.info("Rio app defined. Use 'uv run rio run' to launch.") 