import csv
import logging

from bowtie.constants import DEFAULT_DELIMITER

logger = logging.getLogger(__name__)


def generate(config, output_file, delimiter=DEFAULT_DELIMITER):
    header = config.header

    with open(output_file, "w") as f:
        writer = csv.DictWriter(f, fieldnames=header, delimiter=delimiter)
        writer.writeheader()
