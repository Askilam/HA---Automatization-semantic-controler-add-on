# tests/util.py
from io import StringIO
from ruamel.yaml import YAML
from loader.yaml_load import load_yaml
from converter_IR.ruamel_to_IR import ruamel_to_IR
from analyzer.semantics import apply_rules

def analyze_yaml(yaml_text: str):
    yaml_loader = YAML(typ='safe')
    yaml_loader.preserve_quotes = True

    data = yaml_loader.load(StringIO(yaml_text.strip()))

    automations = ruamel_to_IR(data)

    errors: list = []
    apply_rules(automations, errors=errors)

    return errors