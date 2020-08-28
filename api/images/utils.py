from pathlib import Path
from uuid import uuid4
from functools import partial


def _generate_filename(path, instance, filename):
    random_filename = f"{uuid4().hex}{Path(filename).suffix}"
    return Path(path) / random_filename


generate_image_path_partial = partial(_generate_filename, "images")
