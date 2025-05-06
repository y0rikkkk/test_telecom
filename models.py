from dataclasses import dataclass, field

@dataclass
class Attribute:
    """Represents a single attribute of a UML class."""

    name: str
    type: str



@dataclass
class UmlClass:
    """Represents a UML class as described in the input XML model."""
    name: str
    is_root: bool
    documentation: str
    attributes: list[Attribute] = field(default_factory=list)


@dataclass
class Aggregation:
    """Represents an aggregation relationship between two UML classes."""
    source: str
    target: str
    sourceMultiplicity: str
    targetMultiplicity: str


@dataclass
class UmlStructure:
    """
     Represents the hierarchical structure of UML classes based on aggregation relationships.

    Attributes:
        children (dict[str, list[str]]): Maps each parent class to its list of child class names.
        multiplicities (dict[str, tuple[str, str]]): Maps each class to its (min, max) multiplicity.
    """
    children: dict[str, list[str]] = field(default_factory=dict)
    multiplicities: dict[str, tuple[str, str]] = field(default_factory=dict)

    @staticmethod
    def from_aggregations(aggregations: list[Aggregation]) -> 'UmlStructure':
        """Constructs a UmlStructure instance from a list of aggregation relationships."""
        structure = UmlStructure()
        for agg in aggregations:
            structure.children.setdefault(agg.target, []).append(agg.source)

            if ".." in agg.sourceMultiplicity:
                min_val, max_val = agg.sourceMultiplicity.split("..")
            else:
                min_val = max_val = agg.sourceMultiplicity

            structure.multiplicities[agg.source] = (min_val, max_val)

        return structure

    def get_children(self, class_name: str) -> list[str]:
        return self.children.get(class_name, [])

    def get_multiplicity(self, class_name: str) -> tuple[str, str]:
        return self.multiplicities.get(class_name, ("1", "1"))
