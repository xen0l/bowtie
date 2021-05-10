import logging
import os

import bowtie.schemas

logger = logging.getLogger(__name__)

DEFAULT_SCHEMA = "oisru"
DEFAULT_DELIMITER = ","

DEFAULT_OUTPUT_FORMAT = "png"

SCHEMA_DIR = os.path.dirname(bowtie.schemas.__file__)
SCHEMA_FILE_EXT = ".json"
SUPPORTED_SCHEMAS = [
    os.path.splitext(file)[0]
    for file in os.listdir(f"{SCHEMA_DIR}")
    if file.endswith(SCHEMA_FILE_EXT)
]

# Formats supported by dot, we allow only few of them
SUPPORTED_FORMATS = ["png", "jpg", "svg", "pdf"]
