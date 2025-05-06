import xml.etree.ElementTree as ET
from models import UmlClass, Attribute, Aggregation,UmlStructure

def parse_xml(input_path: str) -> tuple[list[UmlClass], list[Aggregation], UmlStructure]:
    """
    Parses the UML XML model and returns its components.

    Args:
        input_path (str): Path to the XML model file.

    Returns:
        tuple[list[UmlClass], list[Aggregation], UmlStructure]:
            Parsed classes, aggregations, and UML structure.
        """
    tree = ET.parse(input_path)
    root = tree.getroot()

    classes = []
    aggregations = []

    for class_elem in root.findall("Class"):
        name = class_elem.attrib["name"]
        is_root = class_elem.attrib.get("isRoot", "false") == "true"
        documentation = class_elem.attrib.get("documentation", "")
        attributes = []

        for attr in class_elem.findall("Attribute"):
            attr_name = attr.attrib["name"]
            attr_type = attr.attrib["type"]
            attributes.append(Attribute(name=attr_name, type=attr_type))

        classes.append(UmlClass(name=name, is_root=is_root, documentation=documentation, attributes=attributes))

    for agg_elem in root.findall("Aggregation"):
        aggregations.append(Aggregation(
            source=agg_elem.attrib["source"],
            target=agg_elem.attrib["target"],
            sourceMultiplicity=agg_elem.attrib["sourceMultiplicity"],
            targetMultiplicity=agg_elem.attrib["targetMultiplicity"]
        ))
    structure = UmlStructure.from_aggregations(aggregations)

    return classes, aggregations,structure
