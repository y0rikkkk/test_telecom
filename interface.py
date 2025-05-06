from parsers.xml_parser import parse_xml
from generators import generate_meta_json, generate_res_pastched_json, generate_delta_json,generate_config_xml
import os

class Interface:
    """
    Coordinates the full process:
    parsing XML, generating meta/config XML,
    deltas, and applying patches.

    Attributes:
        input_dir (str): Path to the input directory with source files.
        output_dir (str): Path to the output directory for results.
    """
    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.classes = []
        self.aggregations = []
        self.structure = None
        os.makedirs(output_dir, exist_ok=True)


    def run(self):
        self._parse_xml()
        self._generate_meta()
        self._generate_config_xml()
        self._generate_delta()
        self._apply_delta()

    def _parse_xml(self):
        self.classes, self.aggregations, self.structure = parse_xml(f"{self.input_dir}/impulse_test_input.xml")

    def _generate_meta(self):
        generate_meta_json(self.classes, self.structure, f"{self.output_dir}/meta.json")

    def _generate_config_xml(self):
        generate_config_xml(self.classes, self.structure, f"{self.output_dir}/config.xml")

    def _generate_delta(self):
        generate_delta_json(f"{self.input_dir}/config.json", f"{self.input_dir}/patched_config.json", f"{self.output_dir}/delta.json")

    def _apply_delta(self):
        generate_res_pastched_json(f"{self.input_dir}/config.json", f"{self.output_dir}/delta.json", f"{self.output_dir}/res_patched_config.json")