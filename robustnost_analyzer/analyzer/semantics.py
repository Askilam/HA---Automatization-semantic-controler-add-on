# analyzer/semantics.py
from jsonpath_ng.ext import parse
from dataclasses import asdict
import yaml
from typing import List, Dict, Any
from classes.classes import Automation
import datetime
import re

def apply_rules(automations_ir: List[Automation],errors: List[Dict[str, Any]] = None, rules_path: str = 'analyzer/rules.yaml') -> List[Dict[str, Any]]:
    if errors is None:
        errors = []

    with open(rules_path, 'r', encoding='utf-8') as f:
        rules_data = yaml.safe_load(f)
    rules = rules_data.get('rules', []) if rules_data else []

    for idx, auto in enumerate(automations_ir):
        ir_to_dict = asdict(auto)
        for rule in rules:
            query = rule['query']
            try:
                expr = parse(query)
                matches = expr.find(ir_to_dict)
                values = [match.value for match in matches if match.value is not None]
                condition_met = False

                if rule['condition'] == 'exists' and values:
                    if rule['name'] == 'zone_trigg_conf_events':
                        zone_groups = {}
                        for trig in values:
                            entity_id = trig.get('entity_id')
                            zone = trig.get('zone')
                            event = trig.get('event')

                            if entity_id and zone and event:
                                key = (entity_id, zone)
                                if key not in zone_groups:
                                    zone_groups[key] = set()
                                zone_groups[key].add(event)

                        for key, events in zone_groups.items():
                            if {'enter', 'leave'}.issubset(events):
                                condition_met = True
                                break
                    elif rule['name'] == 'repeat_action_while_until':
                        for repeat_action in values:
                            while_ = any(
                                conditio.get('enabled', True) 
                                for conditio in repeat_action.get('while_', [])
                            ) if repeat_action.get('while_') else False

                            until = any(
                                conditio.get('enabled', True) 
                                for conditio in repeat_action.get('until', [])
                            ) if repeat_action.get('until') else False

                            if while_ and until:
                                condition_met = True
                                break
                    elif rule['name'] == 'wait_for_trigger_params': #D8
                        for params in values:
                            if 'to' in params and 'from' not in params and 'for' not in params and 'timeout' not in params:
                                condition_met = True
                            if 'to_' in params and params['to_'] is not None and 'from_' in params and params['from_'] is None:
                                condition_met = True
                    elif rule['name'] == 'wait_for_trigger':

                        all_triggers_expr = parse("$.triggers")
                        all_trigg_matches = all_triggers_expr.find(ir_to_dict)
                        all_triggers = all_trigg_matches[0].value if all_trigg_matches else []
                        
                        for every_wait_trig in values:
                            for wait_trig_vals in every_wait_trig:
                                for one_trig_vals in all_triggers:
                                    if wait_trig_vals == one_trig_vals:
                                        condition_met = True
                                        break
                                        
                                if condition_met:
                                    break
                            if condition_met:
                                break

                    else:
                        for all_val in values:
                            above = all_val.get('above')
                            below = all_val.get('below')
                            if above and below:
                                try:
                                    a = float(above) if isinstance(above, (int, float, str)) else None
                                    b = float(below) if isinstance(below, (int, float, str)) else None
                                    if a is not None and b is not None and a > b:
                                        condition_met = True
                                        break
                                except:
                                    pass
                            else:
                                if above is None and below is not None or above is not None and below is None:
                                    condition_met = False
                                else:
                                    condition_met = True
                elif rule['condition'] == 'empty' and not values:
                    condition_met = True
                elif rule['condition'] == 'equals' and values and all(v == rule.get('value') for v in values):
                    condition_met = True
                elif rule['condition'] == 'contains' and values and any(any(sub in str(v) for sub in rule.get('substring', '').split('|')) for v in values):
                    condition_met = True
                elif rule['condition'] == 'matches_regex' and values and any('{{' in str(v) and re.search(rule.get('regex', ''), str(v)) for v in values if isinstance(v, str)):
                    condition_met = True
                elif rule['condition'] == 'offset' and values:
                    for all_val in values:
                        offset = all_val.get('offset')
                        if offset:
                            try:
                                sign = -1 if offset.startswith('-') else 1
                                string_time = offset.lstrip('+-')
                                hours_, minutes_, seconds_ = map(int, string_time.split(':'))
                                delta_time = datetime.timedelta(hours = hours_, minutes = minutes_, seconds = seconds_) * sign
                                if abs(delta_time) >= datetime.timedelta(days=1):
                                    if all_val.get('event') == 'sunrise' and delta_time < datetime.timedelta(0):
                                        condition_met = True
                                    elif all_val.get('event') == 'sunset' and delta_time > datetime.timedelta(0):
                                        condition_met = True
                                    elif (all_val.get('at') or all_val.get('weekday'))  and delta_time > datetime.timedelta(0):
                                        condition_met = True
                            except:
                                pass

                    
                if condition_met:
                    errors.append({
                        'automation_index': idx,
                        'alias': auto.alias or f"Automation #{idx}",
                        'type': 'semantic',
                        'rule': rule['name'],
                        'message': rule['error']
                    })
            except Exception as e:
                errors.append({
                    'automation_index': idx,
                    'alias': auto.alias or f"Automation #{idx}",
                    'type': 'semantic',
                    'rule': rule['name'],
                    'message': f"Unexpected error in rule '{rule['name']}': {e}"
                })
        
