import xml.etree.ElementTree as ET
from models import UmlClass, UmlStructure

def generate_config_xml(classes: list[UmlClass], structure: UmlStructure, output_path: str) -> None:
    """
    Generates a config.xml file representing the class hierarchy and attributes.

    The function performs a recursive traversal of the UML model starting from the root class.
    Attributes are rendered as XML leaf nodes, and nested classes as nested tags.

    Args:
        classes (list[UmlClass]): List of parsed UML classes.
        structure (UmlStructure): Structure mapping aggregations (parent → children).
        output_path (str): Path to write the resulting XML file.
    """
    class_map = {cls.name: cls for cls in classes}

    root_class = next((cls for cls in classes if cls.is_root))

    def build_element(class_name: str, level: int = 0) -> ET.Element:
        cls = class_map[class_name]
        elem = ET.Element(class_name)

        for attr in cls.attributes:
            attr_elem = ET.SubElement(elem, attr.name)
            attr_elem.text = attr.type

        for child_name in structure.get_children(class_name):
            child_elem = build_element(child_name, level + 1)
            elem.append(child_elem)

        if not cls.attributes and not structure.get_children(class_name):
            elem.text = "\n" + '    ' * level

        return elem

    root_element = build_element(root_class.name)

    tree = ET.ElementTree(root_element)
    ET.indent(tree, space="    ")
    tree.write(output_path, encoding="utf-8", xml_declaration=False, short_empty_elements=False)