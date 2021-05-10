import argparse
import logging
import sys

from bowtie import __description__
from bowtie.config import load_schema_config
from bowtie.constants import (
    DEFAULT_SCHEMA,
    SUPPORTED_SCHEMAS,
    DEFAULT_OUTPUT_FORMAT,
    SUPPORTED_FORMATS,
)
from bowtie.generate import generate
from bowtie.render import render

logger = logging.getLogger(__name__)


def parse_arguments():
    parser = argparse.ArgumentParser(description=__description__)

    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

    # 'generate' subcommand
    generate_parser = subparsers.add_parser(
        "generate", aliases=["gen"], help="Generate CSV file for the selected format"
    )
    generate_parser.add_argument(
        "-s",
        "--schema",
        help="Risk schema to use",
        dest="schema",
        default=DEFAULT_SCHEMA,
        choices=SUPPORTED_SCHEMAS,
    )
    generate_parser.add_argument(
        "file", help="File name", default=f"sample - {DEFAULT_SCHEMA}.csv", nargs="?"
    )

    # 'render' subcommand
    render_parser = subparsers.add_parser(
        "render", aliases=["ren"], help="Render bowtie risk diagram"
    )
    render_parser.add_argument(
        "-s",
        "--schema",
        help="Risk schema to use",
        dest="schema",
        default=DEFAULT_SCHEMA,
        choices=SUPPORTED_SCHEMAS,
    )
    render_parser.add_argument(
        "-f",
        "--format",
        help="Output format to use",
        dest="output_format",
        default=DEFAULT_OUTPUT_FORMAT,
        choices=SUPPORTED_FORMATS,
    )
    render_parser.add_argument(
        "-o", "--output", help="Ouput file", dest="output_file", default="output"
    )
    render_parser.add_argument(
        "file",
        help="Input file",
    )

    args = parser.parse_args()

    if not args.subcommand:
        parser.print_help()
        sys.exit(1)

    return args

def main():
    args = parse_arguments()
    if args.subcommand in ["generate", "gen"]:
        config = load_schema_config(schema=args.schema)
        generate(config=config, output_file=args.file)
    elif args.subcommand in ["render", "ren"]:
        config = load_schema_config(schema=args.schema)

        if args.output_file.endswith(f".{args.output_format}"):
            output_file = args.output_file
        else:
            output_file = f"{args.output_file}.{args.output_format}"

        render(
            config=config,
            output_format=args.output_format,
            output_file=output_file,
            input_file=args.file,
        )
