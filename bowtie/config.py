import json
import logging
import os
from typing import Dict, Any, List

from pydantic import BaseModel

from bowtie.constants import SCHEMA_DIR, SCHEMA_FILE_EXT

logger = logging.getLogger(__name__)


class SchemaConfig(BaseModel):
    header: List[str]
    linkage: List[str]
    style: Dict[str, Any]


def load_schema_config(schema: str):

    schema_file = os.path.join(SCHEMA_DIR, schema + SCHEMA_FILE_EXT)

    with open(schema_file, "r") as f:
        data = json.load(f)

    config = SchemaConfig(**data)

    return config
