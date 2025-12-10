import gspread
import sys
from rdflib import Graph, URIRef, Literal, BNode, Node
from rdflib.namespace import XSD, RDFS, Namespace
from rdflib.util import from_n3
from rdflib.collection import Collection
from urllib.parse import quote
from typing import cast

CREDENTIALS = "credentials.json"

SCOPES = [
    "https://www.googleapis.com/auth/drive.metadata.readonly",
    "https://www.googleapis.com/auth/spreadsheets.readonly",
]

PREFIXES = {
    "": "https://github.com/dkglab/reconstructing-events/",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "ecrm": "http://erlangen-crm.org/current/",
    "bioc": "http://ldf.fi/schema/bioc/",
    "wd": "http://www.wikidata.org/entity/",
    "viaf": "http://viaf.org/viaf/",
}

ECRM = Namespace(PREFIXES["ecrm"])


def expand_curie(curie: str) -> URIRef:
    prefix, reference = curie.split(":", 1)
    if prefix in PREFIXES:
        return URIRef(PREFIXES[prefix] + quote(reference))
    else:
        print(f"Unknown prefix: {prefix}", file=sys.stderr)
        return URIRef("http://example.org/" + prefix + "/" + quote(reference))


def interpret_value(value: str) -> URIRef | Literal:
    if value == "a":
        return interpret_value("rdf:type")
    elif value.startswith("http://") or value.startswith("https://"):
        return URIRef(value)
    elif value.startswith('"'):
        return cast(Literal, from_n3(value))
    elif ":" in value:
        return expand_curie(value)
    else:
        return Literal(value)


def new_blank_node(graph: Graph, value: str) -> BNode:
    subject = BNode()
    for clause in value.strip()[1:-1].split(";"):
        parts = clause.strip().split(" ")
        predicate = interpret_value(parts[0])
        for object in interpret_object(graph, parts[1]):
            add_triple(graph, subject, predicate, object)
    return subject


def new_collection(graph: Graph, value: str) -> BNode:
    subject = BNode()
    items: list[Node] = [interpret_value(v) for v in value[1:-1].strip().split(" ")]
    Collection(graph, subject, items)
    return subject


def interpret_object(graph: Graph, value: str) -> list[URIRef | Literal | BNode]:
    if value.startswith('"'):
        return [cast(Literal, from_n3(value))]
    elif value.startswith("[") and value.endswith("]"):
        return [new_blank_node(graph, value)]
    elif value.startswith("(") and value.endswith(")"):
        return [new_collection(graph, value)]
    else:
        return [interpret_value(v.strip()) for v in value.split(",")]


def strings_to_langstrings(p, o):
    if isinstance(o, Literal):
        if p == RDFS.label:
            return (p, Literal(str(o.value), lang="en"))
    return (p, o)


def dates_to_datetimes(p, o):
    if isinstance(o, Literal) and not o.datatype == XSD.dateTime:
        if p == ECRM.P82a_begin_of_the_begin or p == ECRM.P81a_end_of_the_begin:
            return (p, Literal(str(o.value) + "T00:00:00", datatype=XSD.dateTime))
        if p == ECRM.P82b_end_of_the_end or p == ECRM.P81b_begin_of_the_end:
            return (p, Literal(str(o.value) + "T23:59:59", datatype=XSD.dateTime))
    return (p, o)


def add_triple(g, s, p, o):
    p, o = strings_to_langstrings(p, o)
    p, o = dates_to_datetimes(p, o)
    g.add((s, p, o))


client = gspread.oauth(
    scopes=SCOPES,
    credentials_filename=CREDENTIALS,
)
spreadsheet = client.open(input("The name of your Google sheet: "))
worksheet = spreadsheet.worksheet("Triples")
graph = Graph()

for prefix, namespace in PREFIXES.items():
    graph.namespace_manager.bind(prefix, namespace)

for row in worksheet.get_all_values()[1:]:

    cells = [cell.strip() for cell in row[:3]]
    cells = [cell for cell in cells if len(cell) > 0]
    if len(cells) < 3:
        continue

    try:
        subject = interpret_value(cells[0])
        predicate = interpret_value(cells[1])
        for object in interpret_object(graph, cells[2]):
            add_triple(graph, subject, predicate, object)

    except Exception as e:
        print(
            f"Error processing row {row} in tab {worksheet.title}:\n{cells}\n{e}",
            file=sys.stderr,
        )
        continue

with open(sys.argv[1], "w") as f:
    f.write(graph.serialize(format="ttl"))
