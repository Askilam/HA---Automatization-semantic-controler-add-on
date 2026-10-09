# main.py  (command line version - works exactly as before)
from pprint import pprint #pre print IR potom vymaz
from dataclasses import asdict #pre print IR potom vymaz
import os
from analysis import analyze_file, build_text_report


if __name__ == "__main__":
    automations_ir, errors, problems, recommendations = analyze_file("automatizacia.yaml")

    #IR print terminal iba pre mna
    print("\n=== DEBUG: IR automations ===")
    for i, auto in enumerate(automations_ir):
       pprint(asdict(auto), width=120)

    #errors print terminal iba pre mna pre testovacie ucely
    if errors:
        print("Errors found:")
        for err in errors:
            prefix = "[Semantic errors]" if err.get('type') == 'semantic' else "[Syntax error]"
            rule_part = f" ({err.get('rule')})" if 'rule' in err else ""
            alias_part = f" in automation '{err.get('alias', 'unknown')}'" if err.get('alias') else ""
            print(f"- {prefix}{rule_part}: {err['message']}{alias_part}")
    else:
        print("No errors yaaay :)")

    output_path = os.path.join(os.path.dirname(__file__), "parsed_output.txt")

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(build_text_report(automations_ir, errors, problems, recommendations))
