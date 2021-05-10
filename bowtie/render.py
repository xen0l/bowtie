import csv
import logging

from graphviz import Digraph
from pydantic import create_model, constr

from bowtie.constants import DEFAULT_OUTPUT_FORMAT, DEFAULT_DELIMITER

logger = logging.getLogger(__name__)


def _build_model(config):
    entry_fields = {}
    for item in config.header:
        entry_fields[item] = (constr(min_length=1), ...)
    model = create_model("Entry", **entry_fields)

    return model


def _read_csv(input_file, delimiter):
    contents = []
    with open(input_file, "r") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        for row in reader:
            contents.append(row)

    return contents


def _build_graph(config, data):
    g = Digraph()
    g.graph_attr["rankdir"] = "LR"
    g.graph_attr["splines"] = "polyline"
    g.graph_attr["fontsize"] = "32.0"

    graph_nodes = []
    graph_edges = []

    for item in data:
        for key, value in item.dict().items():
            g.node(value, **config.style[key])

        values = list(item.dict().values())
        graph_edges.extend(list(zip(values, values[1:])))

    graph_nodes = list(set(graph_nodes))
    for node in graph_nodes:
        g.node(node)

    graph_edges = list(set(graph_edges))
    g.edges(graph_edges)
    g.edge_attr["arrowhead"] = "none"

    return g.unflatten()


def render(
    config,
    input_file,
    output_file,
    output_format=DEFAULT_OUTPUT_FORMAT,
    delimiter=DEFAULT_DELIMITER,
):
    Entry = _build_model(config=config)

    file_entries = []
    file_contents = _read_csv(input_file=input_file, delimiter=delimiter)
    for item in file_contents:
        entry = Entry(**item)
        file_entries.append(entry)

    g = _build_graph(config=config, data=file_entries)
    src = g.pipe(format=output_format)
    with open(output_file, "wb") as f:
        f.write(src)
