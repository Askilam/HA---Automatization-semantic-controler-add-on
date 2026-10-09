# analysis.py
# The analysis pipeline from the original main.py, as functions that can be
# used both by the command line (main.py) and by the add-on web page (web.py).
import os
from typing import Any, Dict, List, Tuple

from loader.yaml_load import load_yaml, load_yaml_string
from converter_IR.ruamel_to_IR import ruamel_to_IR
from analyzer.semantics import apply_rules
from analyzer.type_checker import validate_types

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RULES_PATH = os.path.join(BASE_DIR, "analyzer", "rules.yaml")


def analyze_data(raw_data: Any):
    """Run the whole analysis on already loaded YAML data.

    Returns (automations_ir, errors, problems, recommendations).
    """
    errors: List[Dict[str, Any]] = []
    automations_ir = ruamel_to_IR(raw_data if raw_data is not None else [], errors=errors)
    apply_rules(automations_ir, errors=errors, rules_path=RULES_PATH)
    validate_types(automations_ir, errors)

    problems = []
    recommendations = []
    for one in errors:
        mess = one.get('message', '').strip()
        if mess.startswith('Recommendation:'):
            recommendations.append(one)
        elif mess.startswith('Semantic error:'):
            problems.append(one)
    return automations_ir, errors, problems, recommendations


def analyze_file(path: str):
    return analyze_data(load_yaml(path))


def analyze_text(yaml_text: str):
    return analyze_data(load_yaml_string(yaml_text))


def build_text_report(automations_ir, errors, problems, recommendations) -> str:
    """The same text report that main.py has always written to parsed_output.txt."""
    output = []
    output.append("Home Assistant automatisation control - Result")
    output.append("===============================================")
    output.append("")
    output.append(f"Automatisations tested: {len(automations_ir)}")
    output.append("")

    if errors:
        if len(problems) > 0:
            output.append(f"Problems found: {len(problems)}")
            output.append("------------------------\n")
            for i, problem in enumerate(problems, 1):
                alias = problem.get('alias', 'no alias')
                message = problem.get('message')
                output.append(f"{i}.\tAutomatisation:\t{alias}")
                output.append(f"\t{message}")
                output.append("")
        else:
            output.append("Problems found: 0")
            output.append("------------------------\n")
        if len(recommendations) > 0:
            output.append(f"Recommendations found: {len(recommendations)}")
            output.append("------------------------\n")
            for i, problem in enumerate(recommendations, 1):
                alias = problem.get('alias', 'no alias')
                message = problem.get('message')
                output.append(f"{i}.\tAutomatisation:\t{alias}")
                output.append(f"\t{message}")
                output.append("")
        else:
            output.append("Recommendations found: 0")
            output.append("------------------------\n")
    else:
        output.append("No problems/recommendations found\n")
        output.append("Result: OK\n")
    return "\n".join(output)
