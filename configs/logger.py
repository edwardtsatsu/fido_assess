import logging
import os

current_file_path = os.path.abspath(__file__)

script_directory = os.path.dirname(current_file_path)

project_root = os.path.abspath(os.path.join(script_directory, ".."))

logging.basicConfig(
    filename=f"{project_root}/logs/app.log",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)
