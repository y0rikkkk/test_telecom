import json
from models import UmlClass, UmlStructure

def generate_meta_json(classes: list[UmlClass], structure: UmlStructure, output_path: str) -> None:
    """
    Generates meta.json based on UML class structure.

    The file includes metadata for each class: name, documentation, root status,
    multiplicity constraints, and a list of parameters (attributes and nested classes).

    Args:
        classes (list[UmlClass]): Parsed UML classes.
        structure (UmlStructure): Aggregation-based class hierarchy and multiplicities.
        output_path (str): Path to save the resulting meta.json file.
    """
    result = []

    for cls in classes:
        meta_entry = {
            "class": cls.name,
            "documentation": cls.documentation,
            "isRoot": cls.is_root,
        }

        min_val, max_val = structure.get_multiplicity(cls.name)
        meta_entry["min"] = min_val
        meta_entry["max"] = max_val

        parameters = []


        for attr in cls.attributes:
            parameters.append({
                "name": attr.name,
                "type": attr.type
            })

        for child in structure.get_children(cls.name):
            parameters.append({
                "name": child,
                "type": "class"
            })

        meta_entry["parameters"] = parameters
        result.append(meta_entry)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)